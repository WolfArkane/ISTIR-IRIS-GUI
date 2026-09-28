import json


def js_string(value) -> str:
    """
    Encode une valeur Python en littéral JavaScript sûr, utilisable
    directement dans un appel evaluate_js(f"maFonction({js_string(x)})").

    Remplace l'ancien pattern `f"...(`{texte}`)"` qui échappait seulement
    \\ et ` mais laissait passer les séquences `${...}` (injection de
    template literal) et les caractères de contrôle.
    """
    text = str(value)
    encoded = json.dumps(text)  # produit un littéral JS valide (chaîne entre guillemets doubles)
    # U+2028/U+2029 sont valides en JSON mais historiquement problématiques
    # dans certains moteurs JS plus anciens : on les échappe par sécurité.
    encoded = encoded.replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    return encoded
