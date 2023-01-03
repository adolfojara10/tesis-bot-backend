from bot_backend import app, bot, telebot
import threading

def recibir_mensajes():
    bot.infinity_polling()
    

def start_app():
    print("iniciando bot")
    bot.set_my_commands([telebot.types.BotCommand("/start", "Visualizar opciones"),
        telebot.types.BotCommand("/iniciar_sesion","para iniciar sesion con tu cuenta"),
        telebot.types.BotCommand("/foto","para obtener una foto de alguna cámara"),
        telebot.types.BotCommand("/video","para obtener un video de alguna cámara")        
        ])
    # bucle infinito para comprobar si se reciben mensajes nuevos
    hilo_bot = threading.Thread(name="hilo_bot", target=recibir_mensajes)
    hilo_bot.start()

    print("BOOOT INICIADO")
    app.run()


if __name__ == "__main__":
    

    app_thread = threading.Thread(name="app_thread", target=start_app)
    app_thread.start()
    #app.run(debug=True)

    print("app INICIADO")

    

