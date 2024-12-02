import pandas as pd
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

def load_data(file_path):
    # Cargar el archivo CSV
    df = pd.read_csv(file_path)

    # Eliminar espacios en blanco y asegurarnos de que las columnas tengan nombres adecuados
    df.columns = df.columns.str.strip()

    # Asegurar que las fechas estén en formato de fecha
    df['Date'] = pd.to_datetime(df['Date'])

    return df

# Ruta del archivo CSV de ejemplo
file_path = 'bank_statement.csv'
df = load_data(file_path)

# Definir categorías con sus respectivas palabras clave
categories = {
    'Food': ['restaurant', 'coffee', 'supermarket', 'groceries'],
    'Transport': ['taxi', 'uber', 'bus', 'train', 'fuel'],
    'Utilities': ['electricity', 'internet', 'water', 'phone'],
    'Entertainment': ['movie', 'netflix', 'concert'],
    'Healthcare': ['pharmacy', 'doctor']
}

# Función para asignar una categoría a cada transacción
def categorize_expenses(description):
    description = description.lower()
    
    for category, keywords in categories.items():
        if any(keyword in description for keyword in keywords):
            return category
    return 'Others'  # Si no se encuentra ninguna palabra clave

# Aplicar la categorización
df['Category'] = df['Description'].apply(categorize_expenses)

def generate_report(df):
    # Resumen de los gastos por categoría
    summary = df.groupby('Category')['Amount'].sum().reset_index()
    summary = summary.sort_values(by='Amount', ascending=False)

    # Crear gráficos
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Amount', y='Category', data=summary)
    plt.title('Gastos por Categoría')
    plt.xlabel('Monto Total')
    plt.ylabel('Categoría')
    plt.tight_layout()

    # Guardar el gráfico como imagen
    plt.savefig('expenses_by_category.png')

    # Mostrar el reporte en consola
    print("Resumen de Gastos por Categoría:")
    print(summary)

    return summary

# Generar el reporte
generate_report(df)

def send_email(subject, body, to_email, attachment=None):
    from_email = "your_email@example.com"
    password = "your_email_password"

    # Configurar el mensaje
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Adjuntar el cuerpo del mensaje
    msg.attach(MIMEText(body, 'plain'))

    # Si hay un archivo adjunto
    if attachment:
        with open(attachment, 'rb') as file:
            msg.attach(MIMEText(file.read(), 'plain'))

    # Enviar el correo
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print("Correo enviado correctamente!")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

# Enviar el reporte semanal
subject = "Reporte Semanal de Gastos"
body = "Adjunto el reporte semanal de tus gastos categorizados."
send_email(subject, body, "recipient_email@example.com", attachment="expenses_by_category.png")
