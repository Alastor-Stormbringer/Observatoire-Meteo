import sqlite3

connexion = sqlite3.connect("meteo.db")
curseur = connexion.cursor()

# Nombre total de relevés enregistrés
curseur.execute("SELECT COUNT(*) FROM releve")
nombre_releves = curseur.fetchone()[0]
print(f"Nombre total de relevés : {nombre_releves}")

# Température moyenne par ville
curseur.execute("""
    SELECT ville.nom, ROUND(AVG(releve.temperature), 2)
    FROM releve
    JOIN ville ON releve.ville_id = ville.id
    GROUP BY ville.id, ville.nom
""")

print("\nTempérature moyenne par ville :")
for nom, temperature in curseur.fetchall():
    print(f"{nom} : {temperature} °C")

# Température minimale et maximale
curseur.execute("""
    SELECT MIN(temperature), MAX(temperature)
    FROM releve
""")

minimum, maximum = curseur.fetchone()
print(f"\nTempérature minimale : {minimum} °C")
print(f"Température maximale : {maximum} °C")

connexion.close()