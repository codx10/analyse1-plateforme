# -*- coding: utf-8 -*-
"""
Home.py — page d'accueil de la « Plateforme d'apprentissage Analyse 1 ».

Lancement :
    pip install -r requirements.txt
    streamlit run Home.py

Cette page sert de feuille de route : elle explique la méthode, montre les
exercices disponibles et permet de cocher sa progression.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import streamlit as st

from ui import (
    BLEU,
    ORANGE,
    VERT,
    VIOLET,
    carte_stat,
    configurer_page,
    lien_page,
    pied_page,
)

# Dossier du projet : permet de tester si une page existe déjà.
RACINE = Path(__file__).resolve().parent

configurer_page("Accueil", "🏠")


def _html(contenu: str) -> None:
    """Affiche un bloc HTML multiligne (sans que Markdown le prenne pour du code)."""
    st.markdown(textwrap.dedent(contenu).strip(), unsafe_allow_html=True)


def _md_bloc(contenu: str) -> None:
    """Affiche un bloc Markdown multiligne, correctement désindenté."""
    st.markdown(textwrap.dedent(contenu).strip())


# ---------------------------------------------------------------------------
# Barre latérale
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### Analyse 1 · CP1")
    st.caption("ENSA Marrakech · Fonctions réelles")
    st.markdown(
        "Utilise le menu **↑** pour ouvrir une page. "
        "Commence toujours par la **Boîte à outils**."
    )
    st.markdown("---")
    st.caption("Règle d'or : aucune page ne se lit passivement.")


# ---------------------------------------------------------------------------
# 1. Hero
# ---------------------------------------------------------------------------
_html(
    """
    <div class="hero">
        <div class="surtitre">ENSA Marrakech · Cycle ingénieur · CP1</div>
        <h1>Comprendre l'analyse,<br>pas la réciter.</h1>
        <p>
            Une plateforme pour le module <b>Fonctions réelles</b>.
            Pour chaque exercice du TD 3 : le sens de l'énoncé, une image qui
            explique, l'idée de la preuve, la preuve complète, du code pour
            vérifier, les erreurs à éviter et un moyen de retenir.
        </p>
        <span class="puce">10 exercices</span>
        <span class="puce">20 notions</span>
        <span class="puce">7 onglets par exercice</span>
        <span class="puce">quiz + cartes mémoire</span>
    </div>
    """
)

st.write("")


# ---------------------------------------------------------------------------
# 2. Chiffres clés
# ---------------------------------------------------------------------------
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(carte_stat("10", "exercices du TD 3, un par page", BLEU), unsafe_allow_html=True)
with c2:
    st.markdown(carte_stat("20", "notions expliquées dans la boîte à outils", VERT), unsafe_allow_html=True)
with c3:
    st.markdown(carte_stat("7", "onglets pour ne jamais sauter une étape", VIOLET), unsafe_allow_html=True)
with c4:
    st.markdown(carte_stat("0", "corrigé à apprendre par cœur", ORANGE), unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# 3. La méthode
# ---------------------------------------------------------------------------
st.subheader("Comment utiliser la plateforme")
st.markdown(
    "Chaque page d'exercice suit toujours le même chemin. "
    "Ne saute pas d'étape : c'est l'ordre qui fait apprendre."
)

m1, m2, m3 = st.columns(3)
with m1:
    _html(
        """
        <div class="carte">
            <div class="num" style="color:#8ab4ff;font-size:.72rem;letter-spacing:.14em;">ÉTAPE 1</div>
            <div style="font-size:1.05rem;font-weight:700;margin:.25rem 0 .35rem 0;">Je comprends</div>
            <div style="color:#aeb8c6;font-size:.88rem;">
                Je reformule l'énoncé avec mes mots : que me donne-t-on ?
                Que dois-je fabriquer ? Je dessine la situation avant tout calcul.
            </div>
        </div>
        """
    )
with m2:
    _html(
        """
        <div class="carte">
            <div class="num" style="color:#7ee787;font-size:.72rem;letter-spacing:.14em;">ÉTAPE 2</div>
            <div style="font-size:1.05rem;font-weight:700;margin:.25rem 0 .35rem 0;">Je manipule</div>
            <div style="color:#aeb8c6;font-size:.88rem;">
                Je joue avec les curseurs jusqu'à pouvoir <b>prédire</b> ce qui
                va se passer. Une intuition qui se prévoit devient une preuve qui se retrouve.
            </div>
        </div>
        """
    )
with m3:
    _html(
        """
        <div class="carte">
            <div class="num" style="color:#d2b3ff;font-size:.72rem;letter-spacing:.14em;">ÉTAPE 3</div>
            <div style="font-size:1.05rem;font-weight:700;margin:.25rem 0 .35rem 0;">Je restitue</div>
            <div style="color:#aeb8c6;font-size:.88rem;">
                Je ferme l'écran et je réécris la preuve sur une feuille.
                Je compare. Je recommence demain. C'est ça, mémoriser.
            </div>
        </div>
        """
    )

st.write("")
st.info(
    "**La règle des 3 passages.** 1) Je lis pour comprendre. "
    "2) Je refais en regardant seulement les titres des étapes. "
    "3) Je refais seul, puis je rédige comme en DS. "
    "Si le passage 3 bloque, ce n'est pas grave : c'est l'endroit exact à retravailler."
)


# ---------------------------------------------------------------------------
# 4. Les sept onglets et le code couleur
# ---------------------------------------------------------------------------
st.subheader("Les 7 onglets d'une page d'exercice")

g1, g2 = st.columns([1.15, 1], gap="large")
with g1:
    _md_bloc(
        """
        1. **Comprendre l'énoncé** — la version simple, les données, le but.
        2. **Intuition** — un graphique interactif pour voir *pourquoi* c'est vrai.
        3. **Comment trouver l'idée** — le réflexe du prof, pas seulement la solution.
        4. **Preuve complète pas à pas** — chaque étape justifiée, chaque théorème nommé.
        5. **Vérifier avec du code** — Python et SymPy pour contrôler le résultat.
        6. **Erreurs à éviter** — les pièges classiques du devoir.
        7. **À retenir** — un squelette de preuve et 3 questions pour se tester.
        """
    )
with g2:
    _html(
        """
        <div class="carte" style="border-left:5px solid #4c8dff;">
            <b style="color:#9cc0ff;">Bleu</b> — l'intuition, l'image mentale.
        </div><br>
        <div class="carte" style="border-left:5px solid #3fb950;">
            <b style="color:#7ee787;">Vert</b> — une étape de preuve, un exemple.
        </div><br>
        <div class="carte" style="border-left:5px solid #f0883e;">
            <b style="color:#ffb077;">Orange</b> — une erreur fréquente, un contre-exemple.
        </div><br>
        <div class="carte" style="border-left:5px solid #bc8cff;">
            <b style="color:#d2b3ff;">Violet</b> — ce qu'il faut absolument retenir.
        </div>
        """
    )


# ---------------------------------------------------------------------------
# 5. Feuille de route des exercices
# ---------------------------------------------------------------------------
st.subheader("La feuille de route du TD 3")
st.caption("Feuille d'exercices n°3 · Module Fonctions réelles · ENSA Marrakech · M. A. Taoudi")

EXERCICES = [
    {
        "fichier": "01_Ex1.py",
        "titre": "Q, R\\Q et continuité",
        "notions": "Densité · continuité · ε-δ · suites",
        "resume": "Pourquoi h hérite de la continuité seulement si f(x₀) = g(x₀).",
    },
    {
        "fichier": "02_Ex2.py",
        "titre": "Périodicité, monotonie, point fixe",
        "notions": "Limite monotone · TVI · suites",
        "resume": "Trois théorèmes d'existence : aucune limite, une limite, un point fixe unique.",
    },
    {
        "fichier": "03_Ex3.py",
        "titre": "L'équation fonctionnelle de tan",
        "notions": "Densité · continuité · parité",
        "resume": "Résoudre f(x+y) = … sans dériver, avec la formule d'addition de tan.",
    },
    {
        "fichier": "04_Ex4.py",
        "titre": "TVI et Rolle en action",
        "notions": "TVI · Rolle · fonctions auxiliaires",
        "resume": "Quatre questions, quatre réflexes : choisir le bon théorème.",
    },
    {
        "fichier": "05_Ex5.py",
        "titre": "La bijection x/(1+|x|)",
        "notions": "Bijection · réciproque · monotonie",
        "resume": "Fabriquer une bijection de R sur ]−1, 1[ et calculer sa réciproque.",
    },
    {
        "fichier": "06_Ex6.py",
        "titre": "Continuité uniforme",
        "notions": "Continuité uniforme · suites · Heine",
        "resume": "Un seul δ pour tous les points ; pourquoi 1/x résiste.",
    },
    {
        "fichier": "07_Ex7.py",
        "titre": "Prolonger puis dériver",
        "notions": "Prolongement · dérivabilité · C¹",
        "resume": "Boucher un trou, dériver partout, et regarder la dérivée osciller.",
    },
    {
        "fichier": "08_Ex8.py",
        "titre": "Dérivées d'ordre n",
        "notions": "Dérivée n-ième · linéarisation",
        "resume": "sin, cos et sin³ + cos³ : transformer avant de dériver.",
    },
    {
        "fichier": "09_Ex9.py",
        "titre": "TAF et inégalités",
        "notions": "TAF · monotonie · séries",
        "resume": "Majorer des différences, encadrer exp et ln, montrer une divergence.",
    },
    {
        "fichier": "10_Ex10.py",
        "titre": "sin x entre deux droites",
        "notions": "Concavité · TAF · inégalités",
        "resume": "L'inégalité (2/π)x ≤ sin x ≤ x, avec une vraie preuve.",
    },
]

colonne_gauche, colonne_droite = st.columns(2, gap="large")
for indice, exo in enumerate(EXERCICES):
    colonne = colonne_gauche if indice % 2 == 0 else colonne_droite
    chemin = f"pages/{exo['fichier']}"
    disponible = (RACINE / chemin).exists()
    with colonne:
        statut = (
            '<span class="statut ok">disponible</span>'
            if disponible
            else '<span class="statut">en préparation</span>'
        )
        _html(
            f"""
            <div class="carte-exo">
                <div class="num">Exercice {indice + 1}</div>
                <div class="titre">{exo['titre']}</div>
                <div class="notions">{exo['notions']}</div>
                <div style="color:#c9d3e0;font-size:.86rem;margin-top:.45rem;">{exo['resume']}</div>
                {statut}
            </div>
            """
        )
        if disponible:
            lien_page(chemin, "Ouvrir l'exercice →")
        else:
            st.caption("Bientôt disponible : on la construit ensemble, étape par étape.")
        st.write("")


# ---------------------------------------------------------------------------
# 6. Les outils transversaux
# ---------------------------------------------------------------------------
st.subheader("Les outils transversaux")

outils = [
    {
        "fichier": "pages/00_Toolbox.py",
        "titre": "Boîte à outils",
        "texte": "Les 20 définitions et théorèmes du TD, avec une image et un exemple pour chacun.",
        "couleur": BLEU,
    },
    {
        "fichier": "pages/11_Quiz_Flashcards.py",
        "titre": "Quiz & cartes mémoire",
        "texte": "Se tester, espacer les révisions, jouer à « trouve l'erreur ».",
        "couleur": VERT,
    },
    {
        "fichier": "pages/12_Cheat_Sheet.py",
        "titre": "Fiche de synthèse",
        "texte": "Une page de méthodes et de réflexes, à relire la veille du DS.",
        "couleur": VIOLET,
    },
]

outil_cols = st.columns(3, gap="large")
for colonne, outil in zip(outil_cols, outils):
    with colonne:
        _html(
            f"""
            <div class="carte" style="border-left:5px solid {outil['couleur']};">
                <div style="font-size:1.02rem;font-weight:750;margin-bottom:.35rem;">{outil['titre']}</div>
                <div style="color:#aeb8c6;font-size:.87rem;">{outil['texte']}</div>
            </div>
            """
        )
        if (RACINE / outil["fichier"]).exists():
            lien_page(outil["fichier"], "Ouvrir →")
        else:
            st.caption("En préparation.")


# ---------------------------------------------------------------------------
# 7. Progression
# ---------------------------------------------------------------------------
st.subheader("Ma progression")

OBJECTIFS = [
    ("prog_toolbox", "J'ai parcouru les 20 notions de la boîte à outils"),
    ("prog_ex1", "Ex 1 — je sais expliquer le rôle de la densité de Q et R\\Q"),
    ("prog_ex2", "Ex 2 — je sais montrer les trois résultats sans regarder"),
    ("prog_ex3", "Ex 3 — je sais retrouver la forme f(x) = (bˣ−1)/(bˣ+1)"),
    ("prog_ex4", "Ex 4 — je choisis seul entre TVI et Rolle"),
    ("prog_ex5", "Ex 5 — je calcule la réciproque de x/(1+|x|)"),
    ("prog_ex6", "Ex 6 — je sais pourquoi 1/x n'est pas uniformément continue"),
    ("prog_ex7", "Ex 7 — je sais dériver x² sin(1/x) en 0"),
    ("prog_ex8", "Ex 8 — je connais la formule de sin⁽ⁿ⁾"),
    ("prog_ex9", "Ex 9 — je sais appliquer le TAF à une différence"),
    ("prog_ex10", "Ex 10 — je sais prouver (2/π)x ≤ sin x ≤ x"),
    ("prog_quiz", "J'ai fait le quiz et les cartes mémoire"),
    ("prog_cheat", "J'ai relu la fiche de synthèse"),
]


def reinitialiser_progression() -> None:
    """Remet toutes les cases à zéro (appelée par le bouton)."""
    for cle, _ in OBJECTIFS:
        if cle in st.session_state:
            st.session_state[cle] = False


cases_gauche, cases_droite = st.columns(2, gap="large")
for index, (cle, libelle) in enumerate(OBJECTIFS):
    colonne = cases_gauche if index % 2 == 0 else cases_droite
    with colonne:
        st.checkbox(libelle, key=cle)

faits = sum(1 for cle, _ in OBJECTIFS if st.session_state.get(cle, False))
st.progress(faits / len(OBJECTIFS), text=f"{faits} / {len(OBJECTIFS)} objectifs cochés")
st.button("Réinitialiser ma progression", on_click=reinitialiser_progression)
st.caption(
    "La progression est gardée pendant la session. Si tu recharges complètement "
    "la page, elle repart de zéro : c'est volontaire, pour t'éviter de « cocher » "
    "sans avoir révisé."
)


# ---------------------------------------------------------------------------
# 8. Plan de travail et installation
# ---------------------------------------------------------------------------
with st.expander("Un plan de travail sur 7 jours (si tu es pressé)"):
    _md_bloc(
        """
        **Jour 1 — Les fondations.** Boîte à outils : limite, continuité,
        caractérisation séquentielle, densité. Puis Exercice 1.

        **Jour 2 — Existence.** Limite monotone, TVI, point fixe. Exercice 2.

        **Jour 3 — Algèbre et régularité.** Exercice 3 (l'équation de tan),
        puis Exercice 4 (TVI/Rolle). Prends le temps de choisir les fonctions auxiliaires.

        **Jour 4 — Bijections et uniformité.** Exercices 5 et 6.

        **Jour 5 — Dérivation.** Exercices 7 et 8 : prolongement, dérivée n-ième.

        **Jour 6 — Inégalités.** Exercices 9 et 10 : TAF, concavité.

        **Jour 7 — Restitution.** Quiz, cartes mémoire, fiche de synthèse. Tu réécris
        les squelettes de preuve de mémoire, puis tu vérifies.
        """
    )

with st.expander("Installer et lancer la plateforme"):
    _md_bloc(
        """
        Dans un terminal, place-toi dans le dossier du projet, puis :

        ```bash
        pip install -r requirements.txt
        streamlit run Home.py
        ```

        La page s'ouvre dans le navigateur (en général `http://localhost:8501`).
        Il faut Python 3.10 ou plus récent.
        """
    )


# ---------------------------------------------------------------------------
# 9. Mot de la fin
# ---------------------------------------------------------------------------
st.write("")
_html(
    """
    <div class="carte" style="border-left:5px solid #bc8cff;">
        <div style="font-size:1.05rem;font-weight:750;color:#d2b3ff;margin-bottom:.35rem;">
            Le conseil du prof
        </div>
        <div style="color:#c9d3e0;font-size:.95rem;">
            Une preuve n'est pas un texte à réciter : c'est une suite de décisions.
            Si tu sais dire <i>pourquoi</i> on choisit le TVI ici et Rolle là,
            tu n'as plus besoin de retenir la preuve par cœur : tu peux la reconstruire.
        </div>
    </div>
    """
)

pied_page()
