Title: Servidor en django para Google Cloud Messaging para Android (II)
Date: 2014-05-27
Tags: django, android, google-cloud-messaging
Slug: django-android-google-cloud-messaging-server-2
Author: __alexander__

En la [primera parte][django-android-google-cloud-messaging-server-1] mostré el cómo implementar un servidor en django que interactúe con google cloud messages. En esta segunda parte, queda el implementar un cliente en Android que será quien reciba las notificaciones.

Las instrucciones siguientes, toman como referencia el ejemplo publicado en la [documentación][docs-cliente-gcm].

#### Paso 3: Implementando el cliente en android

Creamos un nuevo proyecto cuyo nombre de paquete debe ser el que configuramos en el archivo settings.py del proyecto en django. Luego:

*1.* Añadimos *Google Play Services* a las dependencias, y en caso de que estemos utilizando graddle, el archivo *build.gradle* debería terminar con una sección similar a:

~~~
dependencies {
  compile "com.google.android.gms:play-services:3.1.+"
}
~~~

*2.* Añadimos los permisos al archivo *manifest*:

~~~
::xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.GET_ACCOUNTS" />
<uses-permission android:name="android.permission.WAKE_LOCK" />
<uses-permission android:name="com.google.android.c2dm.permission.RECEIVE" />

<permission android:name="com.alexanderae.demo_gcm.permission.C2D_MESSAGE"
    android:protectionLevel="signature" />
<uses-permission android:name="com.alexanderae.demo_gcm.permission.C2D_MESSAGE" />
~~~

Los dos últimos bloques son para prevenir que alguna aplicación ajena a la nuestra registre o reciba los mensajes que van dirigidos a nuestra app.

*3.* También en el *manifest*, debemos de añadir un *BroadcastReceiver* que capturará el evento de "recibir una notificación" y un Servicio que será lanzado por dicho *receiver*:

~~~
<receiver
    android:name=".GcmBroadcastReceiver"
    android:permission="com.google.android.c2dm.permission.SEND" >
    <intent-filter>
        <action android:name="com.google.android.c2dm.intent.RECEIVE" />
        <category android:name="com.alexanderae.demo_gcm" />
    </intent-filter>
</receiver>
<service android:name=".GcmIntentService" />
~~~

Dentro del bloque *application* debemos incluir la versión de *google play services* a utilizar. Para ello, añadimos el siguiente bloque:

~~~
::xml
<meta-data
    android:name="com.google.android.gms.version"
    android:value="@integer/google_play_services_version" />
~~~

*4.* Creamos una nueva clase que contendrá al receiver que habíamos declarado en el manifest (*GcmBroadcastReceiver.java*):

~~~
::java
public class GcmBroadcastReceiver extends WakefulBroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent) {
        // Especificamos el servicio que manejará el evento
        ComponentName comp = new ComponentName(context.getPackageName(),
                GcmIntentService.class.getName());
        // Inicia el servicio, manteniendo al dispositivo despierto.
        startWakefulService(context, (intent.setComponent(comp)));
        setResultCode(Activity.RESULT_OK);
    }
}
~~~

*5.* Creamos el servicio declarado también en el manifest (*GcmIntentService.java*).
Para este ejemplo, nuestra acción a realizar será el lanzar una notificación:

~~~
::java
public class GcmIntentService extends IntentService {
    public static final int NOTIFICATION_ID = 1;
    NotificationManager mNotificationManager;
    String TAG = "GcmIntentService";

    public GcmIntentService() {
        super("GcmIntentService");
    }

    @Override
    protected void onHandleIntent(Intent intent) {
        Bundle extras = intent.getExtras();
        GoogleCloudMessaging gcm = GoogleCloudMessaging.getInstance(this);
        // El parámetro intent de getMessageType() debe ser el intent enviado por el
        // BroadcastReceiver.
        String messageType = gcm.getMessageType(intent);

        if (!extras.isEmpty()) {
            /*
             * Filtramos los mensajes basados en el tipo (aparentemente en un futuro cercano, se
             * añadirán tipos de mensajes)
             */
            if (GoogleCloudMessaging.
                    MESSAGE_TYPE_SEND_ERROR.equals(messageType)) {
                sendNotification("Send error: " + extras.toString());
            } else if (GoogleCloudMessaging.
                    MESSAGE_TYPE_DELETED.equals(messageType)) {
                sendNotification("Deleted messages on server: " +
                        extras.toString());
                // Si es un mensaje normal, ejecutamos la acción deseada.
            } else if (GoogleCloudMessaging.
                    MESSAGE_TYPE_MESSAGE.equals(messageType)) {
                // Lanzamos la notificación
                sendNotification("Received: " + extras.toString());
                Log.i(TAG, "Received: " + extras.toString());
            }
        }
        // Liberamos el bloqueo
        GcmBroadcastReceiver.completeWakefulIntent(intent);
    }

    // A modo de ejemplo, lanzamos una notificación al recibir el mensaje..
    // Podemos realizar cualquier otra acción según nuestras necesidades.
    private void sendNotification(String msg) {
        mNotificationManager = (NotificationManager)
                this.getSystemService(Context.NOTIFICATION_SERVICE);

        PendingIntent contentIntent = PendingIntent.getActivity(this, 0,
                new Intent(this, MainActivity.class), 0);

        NotificationCompat.Builder mBuilder =
                new NotificationCompat.Builder(this)
                        .setSmallIcon(R.drawable.ic_launcher)
                        .setContentTitle("Notificación GCM")
                        .setStyle(new NotificationCompat.BigTextStyle()
                                .bigText(msg))
                        .setContentText(msg);

        mBuilder.setContentIntent(contentIntent);
        mNotificationManager.notify(NOTIFICATION_ID, mBuilder.build());
    }
}
~~~

*6.* En nuestro *MainActivity*:

Agregamos algunas variables y constantes a utilizar:

~~~
::java
TextView mDisplay; // debemos añadir un TextView al layout
GoogleCloudMessaging gcm;
Context context;

private final static int PLAY_SERVICES_RESOLUTION_REQUEST = 9000;
String regid; // ID asignado por GCM para el dispositivo
String TAG = "MainActivity";
String SENDER_ID = "160161620856"; // ID del Proyecto obtenido de la consola de desarrolladores
// de Google
String NAMESPACE = "http://192.168.1.35:8001/gcm/"; // URL del servidor GCM (django)

public static final String PROPERTY_REG_ID = "registration_id";
private static final String PROPERTY_APP_VERSION = "appVersion";
~~~

En el *onCreate* verificamos que *[Google Play Services][google-play-services]* esté instalado, en caso afirmativo, continuamos recuperando el *código de registro*, caso contrario, llamamos a la función *registerInBackground* para crear un nuevo código.

Se nos recomienda que verifiquemos que *GPS* (Google Play Services) esté instalado en cada llamada al evento *onResume*:

~~~
::java
@Override
protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_main);

    mDisplay = (TextView) findViewById(R.id.display);

    context = getApplicationContext();

    // Verifica que Google Play Services esté instalado
    if (checkPlayServices()) {
        gcm = GoogleCloudMessaging.getInstance(this);
        regid = getRegistrationId(context);

        if (regid.isEmpty()) {
            registerInBackground();
        }
    } else {
        Log.i(TAG, "No se encontró Google Play Services.");
    }
}

@Override
protected void onResume() {
    super.onResume();
    checkPlayServices();
}
~~~

Agregamos las funciones que verifican la instalación de *GPS*, la que obtiene el código de registro (*getRegistrationId* + *getGCMPreferences*) y la que obtiene la versión de la aplicación (*getAppVersion*):

~~~
::java
// Verifica que Google Play Services esté instalado.
private boolean checkPlayServices() {
    int resultCode = GooglePlayServicesUtil.isGooglePlayServicesAvailable(this);
    if (resultCode != ConnectionResult.SUCCESS) {
        if (GooglePlayServicesUtil.isUserRecoverableError(resultCode)) {
            GooglePlayServicesUtil.getErrorDialog(resultCode, this,
                    PLAY_SERVICES_RESOLUTION_REQUEST).show();
        } else {
            Log.i(TAG, "Dispositivo no soportado!");
            finish();
        }
        return false;
    }
    return true;
}

// Obtiene el código de registro
private String getRegistrationId(Context context) {
    final SharedPreferences prefs = getGCMPreferences();

    String registrationId = prefs.getString(PROPERTY_REG_ID, "");
    if (registrationId.isEmpty()) {
        Log.i(TAG, "Registro no encontrado");
        return "";
    }
    // Verifica si la aplicación fue actualizada, en cuyo caso, se debe volver a generar
    // un código de registro.
    int registeredVersion = prefs.getInt(PROPERTY_APP_VERSION, Integer.MIN_VALUE);
    int currentVersion = getAppVersion(context);
    if (registeredVersion != currentVersion) {
        Log.i(TAG, "La versión de la aplicación ha cambiado.");
        return "";
    }
    return registrationId;
}

// Obtiene el código de registro desde los SharedPreferences
private SharedPreferences getGCMPreferences() {
    return getSharedPreferences(MainActivity.class.getSimpleName(),
            Context.MODE_PRIVATE);
}

// Obtiene la versión actual de la aplicación
private static int getAppVersion(Context context) {
    try {
        PackageInfo packageInfo = context.getPackageManager()
                .getPackageInfo(context.getPackageName(), 0);
        return packageInfo.versionCode;
    } catch (PackageManager.NameNotFoundException e) {
        throw new RuntimeException("No se encontró el nombre del paquete: " + e);
    }
}
~~~

Por último, añadimos el *AsyncTask* que realiza el registro en *GCM* (registerInBackground), la función que envía el ID a nuestro servidor (*sendRegistrationIdToBackend*) y la que almacena el código en los SharedPreferences (*storeRegistrationId*):

~~~
::java
private void registerInBackground() {

    class RegistroGCM extends AsyncTask<Void, Void, String> {

        @Override
        protected String doInBackground(Void... params) {
            String msg;
            try {
                if (gcm == null) {
                    gcm = GoogleCloudMessaging.getInstance(context);
                }
                regid = gcm.register(SENDER_ID);
                msg = "Device registered, registration ID=" + regid;

                // Enviamos el código de registro a nuestro servidor
                sendRegistrationIdToBackend(regid);

                // Almacenamos el código de registro
                storeRegistrationId(context, regid);
            } catch (IOException ex) {
                msg = "Error :" + ex.getMessage();
                // Si hay un error, se debe informar al usuario para que realize
                // una acción adecuada.
            }
            return msg;
        }

        @Override
        protected void onPostExecute(String msg) {
            mDisplay.append(msg + "\n");
        }
    }

    RegistroGCM registro = new RegistroGCM();
    registro.execute();
}


private void sendRegistrationIdToBackend(String regid) {
    String url_registro = NAMESPACE + "registra-usuario?usuario_id=" + regid;

    HttpClient client = new DefaultHttpClient();
    HttpGet get = new HttpGet(url_registro);

    try {
        HttpResponse response = client.execute(get);
        Log.i(TAG, "response: " + response);
    } catch (Exception e) {
        Log.d(TAG, "Error de registro en mi servidor: " + e.getCause() + " || " + e.getMessage());
    }
}

// Almacena el código de registro en los SharedPreferences
private void storeRegistrationId(Context context, String regId) {
    final SharedPreferences prefs = getGCMPreferences();
    int appVersion = getAppVersion(context);
    Log.i(TAG, "Saving regId on app version " + appVersion);
    SharedPreferences.Editor editor = prefs.edit();
    editor.putString(PROPERTY_REG_ID, regId);
    editor.putInt(PROPERTY_APP_VERSION, appVersion);
    editor.commit();
}
~~~

Y con ello, ya podríamos realizar las pruebas respectivas desde nuestro servidor en django.

*Nota:* No he creado un repositorio para este proyecto en android, pero ya que es prácticamente idéntico al de la documentaciñón, se puede consultar el [repositorio de google][google-code-repo].

[django-android-google-cloud-messaging-server-1]: /django-android-google-cloud-messaging-server-1.html
[docs-cliente-gcm]: http://developer.android.com/google/gcm/client.html
[google-code-repo]: https://code.google.com/p/gcm/source/browse/
[google-play-services]: http://developer.android.com/google/play-services/index.html