
# --- REGLAS DEL AGENTE DE ESTUDIO ---

acciones_estudio = {

    # Básicas
    'login': '¡Hola! Bienvenido de nuevo, ¿listo para estudiar?',
    'login,tareas': 'Veo que tienes tareas pendientes. Te las muestro para que organices tu tiempo.',
    'login,tareas,urgente': '¡Atención! Tienes tareas con fecha límite cercana. Te recomiendo empezar por esas.',

    # Estado
    'login,energia-baja': 'Parece que estás cansado. Te recomendaría iniciar con algo suave o tomar un breve descanso.',
    'login,tiempo-corto': 'Tu tiempo es limitado, así que enfoquémonos en lo más importante.',
    'login,motivado': '¡Excelente energía! Aprovechemos esa motivación para avanzar mucho hoy.',
    'login,tareas,dificil': 'Hay tareas difíciles. Te sugiero dividirlas en pasos pequeños.',

    # Sin login
    'tareas': 'Parece que tienes tareas, pero tienes que iniciar sesión para verlas.',
    'tareas,urgente': '¡Puedes tener tareas urgentes, necesitas iniciar sesión!',
    'tareas,completado': 'Genial que completaste una tarea, pero aún no has iniciado sesión. No se quien eres.',

    # Secuencias largas existentes
    'login,tareas,energia-baja,urgente': 'Sé que estás cansado, pero tienes tareas urgentes. Vamos a priorizar solo lo esencial.',
    'login,tareas,motivado,urgente': 'Tienes motivación y tareas urgentes. ¡Perfecto! Vamos con toda.',
    'login,tareas,tiempo-corto,urgente': 'Tienes poco tiempo y tareas urgentes: te prepararé un plan rápido y eficiente.',

    # --- CON 'completado' ---
    'login,tareas,completado': '¡Excelente trabajo! Terminaste una tarea.',

    'login,tareas,urgente,completado': '¡Muy bien! Completaste una tarea urgente. Eso quita presión.',

    'login,tareas,motivado,completado': '¡Se nota tu motivación! Tarea completada sin problemas.',
    'login,tareas,motivado,urgente,completado': '¡Impresionante! Terminaste la más urgente gracias a tu motivación.',

    'login,tareas,energia-baja,completado': '¡Bien hecho! Y eso que estabas cansado. Quizá mereces un descanso.',
    'login,tareas,energia-baja,urgente,completado': 'Terminaste la urgente aun estando cansado… ¡muy buen esfuerzo!',

    'login,tareas,tiempo-corto,completado': 'Con poco tiempo lograste completar una tarea. Bien hecho.',
    'login,tareas,tiempo-corto,urgente,completado': 'Con poco tiempo completaste la urgente. Muy eficiente.',

    'login,tareas,dificil,completado': 'Esa tarea difícil ya está lista. ¡Felicidades!',
    'login,tareas,dificil,urgente,completado': '¡Gran logro! Tarea difícil y urgente completada.'
}

# --- CLASE DEL AGENTE ---
class AgenteEstudio:

    def __init__(self, acciones):
        self.acciones = acciones
        self.percepciones = ''

    def es_prefijo_valido(self, percepcion_concat):
        """Valida si la cadena es un prefijo de alguna clave existente."""
        for key in self.acciones.keys():
            if key.startswith(percepcion_concat):
                return True
        return False

    def actuar(self, percepcion, accion_basica='No tengo sugerencias para esa combinación aún.'):
        if not percepcion:
            return accion_basica

        nueva_cadena = (
            self.percepciones + ',' + percepcion
            if self.percepciones else percepcion
        )

        if not (nueva_cadena in self.acciones or self.es_prefijo_valido(nueva_cadena)):
            self.percepciones = ''
            return (
                f"La combinación '{nueva_cadena}' no es válida.\n"
                "He reiniciado las percepciones. Intenta otra secuencia."
            )

        self.percepciones = nueva_cadena

        if self.percepciones in self.acciones:
            return self.acciones[self.percepciones]

        return f"Percepción añadida: {percepcion}. Continúa..."
    
    def reiniciar(self):
        self.percepciones = ''
        return "Percepciones reiniciadas. ¡Vamos de nuevo!"

# Instancia del agente
asistente = AgenteEstudio(acciones_estudio)

# Interfaz con Gradio

import gradio as gr

def procesar_percepcion(percepcion):
    accion = asistente.actuar(percepcion)
    return (
        f"{accion}\n\n Percepciones actuales: {asistente.percepciones or '—'}",
        gr.update(value="")  
    )

def reiniciar_percepciones():
    return asistente.reiniciar()


# Interfaz
with gr.Blocks(title="Agente Inteligente de Estudio") as iface:
    gr.Markdown(
        """
        #  Agente Inteligente de Estudio  
        Escribe percepciones como **login**, **tareas**, **urgente**, **motivado**,  
        **energia-baja**, **tiempo-corto**, **dificil**, etc.

        El agente responderá de forma **conversacional** según las percepciones acumuladas.
        """
    )

    with gr.Row():
        entrada = gr.Textbox(
            label="Ingresa percepción",
            placeholder="Ej: login, tareas, urgente...",
            lines=3
        )

    with gr.Row():
        btn_enviar = gr.Button("Procesar percepción", variant="primary")
        btn_reiniciar = gr.Button(" Reiniciar percepciones", variant="secondary")

    salida = gr.Textbox(
        label="Respuesta del agente",
        lines=6
    )

    btn_enviar.click(
    fn=procesar_percepcion,
    inputs=entrada,
    outputs=[salida, entrada]
)
    btn_reiniciar.click(fn=reiniciar_percepciones, outputs=salida)

iface.launch()