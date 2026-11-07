from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "change-this-secret-key"
DB = Path(__file__).with_name("carnet.db")

def connect():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    with connect() as con:
        con.executescript("""
        CREATE TABLE IF NOT EXISTS profile (
          id INTEGER PRIMARY KEY, nom TEXT, prenom TEXT, naissance TEXT,
          adresse TEXT, telephone TEXT, email TEXT
        );
        CREATE TABLE IF NOT EXISTS appointments (
          id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT NOT NULL,
          heure TEXT, service TEXT, lieu TEXT, statut TEXT DEFAULT 'À venir'
        );
        CREATE TABLE IF NOT EXISTS medical_records (
          id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, type TEXT,
          titre TEXT, description TEXT, lieu TEXT
        );
        CREATE TABLE IF NOT EXISTS reminders (
          id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, titre TEXT,
          details TEXT, statut TEXT DEFAULT 'À faire'
        );
        CREATE TABLE IF NOT EXISTS breast_cancer_followup (
          id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT NOT NULL,
          suivi_type TEXT NOT NULL, professionnel TEXT, traitement TEXT,
          examen_resultat TEXT, prochain_rdv TEXT, notes TEXT
        );
        CREATE TABLE IF NOT EXISTS vaccinations (
          id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT NOT NULL,
          vaccin TEXT NOT NULL, dose TEXT, lot TEXT, professionnel TEXT,
          prochain_rappel TEXT, notes TEXT
        );
        """)
        if not con.execute("SELECT id FROM profile").fetchone():
            con.execute("INSERT INTO profile (nom,prenom,naissance,adresse,telephone,email) VALUES (?,?,?,?,?,?)",
                        ("Daghmani","Amal","10/05/2003","Dakhla","06 66 51 80 22","amal@example.com"))
        if not con.execute("SELECT id FROM appointments").fetchone():
            con.execute("INSERT INTO appointments (date,heure,service,lieu) VALUES (?,?,?,?)",
                        ("2026-11-15","10:00","Consultation gynécologique","CHR Dakhla"))
        if not con.execute("SELECT id FROM medical_records").fetchone():
            con.execute("INSERT INTO medical_records (date,type,titre,description,lieu) VALUES (?,?,?,?,?)",
                        ("2026-10-12","Consultation","Consultation gynécologique","Exemple de dossier — données fictives","CHR Dakhla"))

@app.route("/")
def home():
    with connect() as con:
        profile = con.execute("SELECT * FROM profile LIMIT 1").fetchone()
        appointments = con.execute("SELECT * FROM appointments ORDER BY date LIMIT 5").fetchall()
        records_count = con.execute("SELECT COUNT(*) n FROM medical_records").fetchone()["n"]
        reminders_count = con.execute("SELECT COUNT(*) n FROM reminders WHERE statut='À faire'").fetchone()["n"]
    return render_template("index.html", profile=profile, appointments=appointments,
                           records_count=records_count, reminders_count=reminders_count, page="Accueil")

@app.route("/profil", methods=["GET","POST"])
def profil():
    with connect() as con:
        if request.method == "POST":
            fields = ("nom","prenom","naissance","adresse","telephone","email")
            values = [request.form.get(f,"").strip() for f in fields]
            con.execute("UPDATE profile SET nom=?,prenom=?,naissance=?,adresse=?,telephone=?,email=? WHERE id=1", values)
            flash("Profil mis à jour.")
            return redirect(url_for("profil"))
        profile = con.execute("SELECT * FROM profile LIMIT 1").fetchone()
    return render_template("profil.html", profile=profile, page="Mon profil")

@app.route("/dossier", methods=["GET","POST"])
def dossier():
    with connect() as con:
        if request.method == "POST":
            con.execute("INSERT INTO medical_records (date,type,titre,description,lieu) VALUES (?,?,?,?,?)",
                        tuple(request.form.get(k,"").strip() for k in ("date","type","titre","description","lieu")))
            flash("Élément ajouté au carnet médical.")
            return redirect(url_for("dossier"))
        records = con.execute("SELECT * FROM medical_records ORDER BY date DESC").fetchall()
    return render_template("dossier.html", records=records, page="Mon carnet médical")

@app.route("/rendez-vous", methods=["GET","POST"])
def rendezvous():
    with connect() as con:
        if request.method == "POST":
            con.execute("INSERT INTO appointments (date,heure,service,lieu) VALUES (?,?,?,?)",
                        tuple(request.form.get(k,"").strip() for k in ("date","heure","service","lieu")))
            flash("Rendez-vous ajouté.")
            return redirect(url_for("rendezvous"))
        appointments = con.execute("SELECT * FROM appointments ORDER BY date,heure").fetchall()
    return render_template("appointments.html", appointments=appointments, page="Rendez-vous")

@app.route("/rappels", methods=["GET","POST"])
def rappels():
    with connect() as con:
        if request.method == "POST":
            con.execute("INSERT INTO reminders (date,titre,details) VALUES (?,?,?)",
                        tuple(request.form.get(k,"").strip() for k in ("date","titre","details")))
            flash("Rappel ajouté.")
            return redirect(url_for("rappels"))
        reminders = con.execute("SELECT * FROM reminders ORDER BY date").fetchall()
    return render_template("reminders.html", reminders=reminders, page="Rappels & Notifications")


@app.route("/suivi-cancer-sein", methods=["GET","POST"])
def suivi_cancer_sein():
    with connect() as con:
        if request.method == "POST":
            con.execute("""INSERT INTO breast_cancer_followup
                (date,suivi_type,professionnel,traitement,examen_resultat,prochain_rdv,notes)
                VALUES (?,?,?,?,?,?,?)""",
                tuple(request.form.get(k,"").strip() for k in
                      ("date","suivi_type","professionnel","traitement","examen_resultat","prochain_rdv","notes")))
            flash("Suivi ajouté.")
            return redirect(url_for("suivi_cancer_sein"))
        suivis = con.execute("SELECT * FROM breast_cancer_followup ORDER BY date DESC, id DESC").fetchall()
    return render_template("suivi_cancer_sein.html", suivis=suivis, page="Suivi cancer du sein")


@app.route("/vaccination", methods=["GET","POST"])
def vaccination():
    with connect() as con:
        if request.method == "POST":
            con.execute("""INSERT INTO vaccinations
                (date,vaccin,dose,lot,professionnel,prochain_rappel,notes)
                VALUES (?,?,?,?,?,?,?)""",
                tuple(request.form.get(k,"").strip() for k in
                      ("date","vaccin","dose","lot","professionnel","prochain_rappel","notes")))
            flash("Vaccination enregistrée.")
            return redirect(url_for("vaccination"))
        vaccins = con.execute("SELECT * FROM vaccinations ORDER BY date DESC, id DESC").fetchall()
    return render_template("vaccination.html", vaccins=vaccins, page="Vaccination")

@app.route("/conseils")
def conseils():
    tips = [
        ("Alimentation","Privilégiez une alimentation variée, équilibrée et une bonne hydratation."),
        ("Dépistage","Respectez les recommandations locales de dépistage et demandez conseil à un professionnel."),
        ("Suivi de grossesse","Le suivi prénatal doit être réalisé auprès d’un professionnel de santé."),
        ("Activité physique","Une activité adaptée et régulière contribue au bien-être général.")
    ]
    return render_template("tips.html", tips=tips, page="Conseils santé")

@app.route("/documents")
def documents():
    return render_template("documents.html", page="Documents")

@app.route("/parametres")
def parametres():
    return render_template("settings.html", page="Paramètres")

init_db()

if __name__ == "__main__":
    app.run(debug=True)
