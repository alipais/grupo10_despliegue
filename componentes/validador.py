import re

def validar_contraseña(password):
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres."
    if not re.search("[A-Z]", password):
        return False, "La contraseña debe contener al menos una letra mayúscula."
    if not re.search("[^a-zA-Z0-9]", password):
        return False, "La contraseña debe contener al menos un carácter especial."
    return True, ""

def validar_nombre(nombre):
    if re.search("[0-9]", nombre):
        return False, "El nombre no puede contener numeros."
    return True, ""