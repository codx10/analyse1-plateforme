# -*- coding: utf-8 -*-
"""
ui.py — l'habillage commun de la « Plateforme d'apprentissage Analyse 1 ».

Toutes les pages importent ce fichier pour :
  * configurer la page et injecter le style (thème sombre, encadrés colorés) ;
  * afficher des encadrés pédagogiques (bleu, vert, orange, violet) ;
  * afficher un graphique Plotly avec le même look ;
  * poser une mini-question avec la réponse cachée.

Les commentaires sont en français : c'est aussi un exemple de code lisible.
"""

from __future__ import annotations

import inspect
import textwrap
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st


# ---------------------------------------------------------------------------
# 1. Palette de couleurs
# ---------------------------------------------------------------------------
# Une seule palette pour toute la plateforme : les pages restent cohérentes.
BLEU = "#4c8dff"      # intuition
VERT = "#3fb950"      # preuve / exemple
ORANGE = "#f0883e"    # erreur fréquente / contre-exemple
VIOLET = "#bc8cff"    # à retenir
ROUGE = "#ff6b6b"     # alerte
JAUNE = "#e3b341"     # remarque
GRIS = "#8b949e"      # éléments secondaires
TEXTE = "#e6edf3"
FOND = "#0e1117"

COULEURS_ENCADRE = {
    "bleu": BLEU,
    "vert": VERT,
    "orange": ORANGE,
    "violet": VIOLET,
    "rouge": ROUGE,
}

TITRES_ENCADRE = {
    "bleu": "Intuition",
    "vert": "Preuve",
    "orange": "Erreur fréquente",
    "violet": "À retenir",
    "rouge": "Attention",
}


# ---------------------------------------------------------------------------
# 2. Feuille de style
# ---------------------------------------------------------------------------
# Astuce : Streamlit ne permet pas de colorer directement un conteneur.
# On place donc un petit repère invisible (span.marqueur-...) dans le conteneur,
# puis le CSS ":has(...)" colore le conteneur qui contient ce repère.
CSS = """
<style>
/* ---------- base ---------- */
html, body, [class*="css"] {
    font-family: "Inter", "Segoe UI", "Helvetica Neue", Arial, sans-serif;
}
.stApp {
    background:
        radial-gradient(1100px 520px at 12% -10%, rgba(76, 141, 255, 0.14), transparent 60%),
        radial-gradient(900px 460px at 92% 0%, rgba(188, 140, 255, 0.10), transparent 55%),
        #0e1117;
}
.block-container {
    padding-top: 2.2rem;
    padding-bottom: 4rem;
    max-width: 1180px;
}
h1, h2, h3, h4 {
    color: #f2f6fb;
    letter-spacing: -0.015em;
}
h1 { font-size: 2.15rem; }
h2 { font-size: 1.55rem; margin-top: 1.6rem; }
h3 { font-size: 1.18rem; }
p, li, label, .stMarkdown {
    line-height: 1.68;
}
a { color: #8ab4ff; }

/* ---------- barre latérale ---------- */
section[data-testid="stSidebar"] {
    background: #0b0f16;
    border-right: 1px solid rgba(255, 255, 255, 0.06);
}
section[data-testid="stSidebar"] .block-container {
    padding-top: 1.2rem;
}

/* ---------- en-tête de page ---------- */
.entete {
    margin-bottom: 1.1rem;
}
.entete .surtitre {
    font-size: 0.76rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #8ab4ff;
    font-weight: 700;
    margin-bottom: 0.25rem;
}
.entete h1 {
    margin: 0.1rem 0 0.35rem 0;
    font-size: 2.15rem;
    line-height: 1.18;
}
.entete p {
    color: #b9c2cf;
    font-size: 1.02rem;
    margin: 0;
    max-width: 880px;
}

/* ---------- hero de l'accueil ---------- */
.hero {
    position: relative;
    overflow: hidden;
    padding: 2.3rem 2.4rem 2.1rem 2.4rem;
    border-radius: 24px;
    border: 1px solid rgba(122, 162, 247, 0.28);
    background:
        linear-gradient(135deg, rgba(76, 141, 255, 0.18), rgba(188, 140, 255, 0.10) 55%, rgba(63, 185, 80, 0.07));
    box-shadow: 0 18px 50px rgba(0, 0, 0, 0.25);
}
.hero::after {
    content: "";
    position: absolute;
    width: 340px;
    height: 340px;
    right: -120px;
    top: -140px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(76, 141, 255, 0.28), transparent 65%);
}
.hero .surtitre {
    font-size: 0.76rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #9cc0ff;
    font-weight: 700;
}
.hero h1 {
    font-size: 2.7rem;
    line-height: 1.12;
    margin: 0.55rem 0 0.7rem 0;
}
.hero p {
    color: #c9d3e0;
    font-size: 1.06rem;
    max-width: 760px;
    margin-bottom: 0.9rem;
}
.puce {
    display: inline-block;
    padding: 0.28rem 0.72rem;
    margin: 0.15rem 0.28rem 0.15rem 0;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.055);
    border: 1px solid rgba(255, 255, 255, 0.11);
    color: #cdd6e3;
    font-size: 0.79rem;
}

/* ---------- cartes ---------- */
.carte {
    background: rgba(22, 27, 38, 0.72);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 1.05rem 1.15rem;
    height: 100%;
    transition: border-color 0.15s ease, transform 0.15s ease;
}
.carte:hover {
    border-color: rgba(122, 162, 247, 0.45);
    transform: translateY(-1px);
}
.carte-stat {
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.045), rgba(255, 255, 255, 0.015));
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 1rem 1.1rem;
    text-align: left;
    height: 100%;
}
.carte-stat .valeur {
    font-size: 1.7rem;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 0.35rem;
}
.carte-stat .libelle {
    color: #aeb8c6;
    font-size: 0.82rem;
    line-height: 1.35;
}
.carte-exo {
    background: rgba(22, 27, 38, 0.72);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-left: 4px solid #4c8dff;
    border-radius: 14px;
    padding: 0.95rem 1.05rem 0.85rem 1.05rem;
    height: 100%;
}
.carte-exo .num {
    font-size: 0.72rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #8ab4ff;
    font-weight: 700;
}
.carte-exo .titre {
    font-size: 1.02rem;
    font-weight: 700;
    color: #eef3fa;
    margin: 0.2rem 0 0.3rem 0;
    line-height: 1.3;
}
.carte-exo .notions {
    color: #aeb8c6;
    font-size: 0.84rem;
    line-height: 1.45;
}
.carte-exo .statut {
    display: inline-block;
    margin-top: 0.55rem;
    font-size: 0.72rem;
    padding: 0.15rem 0.5rem;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.06);
    color: #b9c2cf;
}
.carte-exo .statut.ok {
    background: rgba(63, 185, 80, 0.14);
    color: #7ee787;
}

/* ---------- encadrés pédagogiques ---------- */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 15px;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.marqueur-bleu) {
    background: linear-gradient(180deg, rgba(76, 141, 255, 0.13), rgba(76, 141, 255, 0.045));
    border: 1px solid rgba(76, 141, 255, 0.34);
    border-left: 5px solid #4c8dff;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.marqueur-vert) {
    background: linear-gradient(180deg, rgba(63, 185, 80, 0.12), rgba(63, 185, 80, 0.04));
    border: 1px solid rgba(63, 185, 80, 0.34);
    border-left: 5px solid #3fb950;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.marqueur-orange) {
    background: linear-gradient(180deg, rgba(240, 136, 62, 0.12), rgba(240, 136, 62, 0.04));
    border: 1px solid rgba(240, 136, 62, 0.36);
    border-left: 5px solid #f0883e;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.marqueur-violet) {
    background: linear-gradient(180deg, rgba(188, 140, 255, 0.13), rgba(188, 140, 255, 0.045));
    border: 1px solid rgba(188, 140, 255, 0.36);
    border-left: 5px solid #bc8cff;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.marqueur-rouge) {
    background: linear-gradient(180deg, rgba(255, 107, 107, 0.12), rgba(255, 107, 107, 0.04));
    border: 1px solid rgba(255, 107, 107, 0.36);
    border-left: 5px solid #ff6b6b;
}
.marqueur-bleu, .marqueur-vert, .marqueur-orange,
.marqueur-violet, .marqueur-rouge {
    display: none;
}
.titre-encadre {
    font-weight: 750;
    font-size: 1.02rem;
    letter-spacing: 0.01em;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.marqueur-bleu) .titre-encadre { color: #9cc0ff; }
div[data-testid="stVerticalBlockBorderWrapper"]:has(.marqueur-vert) .titre-encadre { color: #7ee787; }
div[data-testid="stVerticalBlockBorderWrapper"]:has(.marqueur-orange) .titre-encadre { color: #ffb077; }
div[data-testid="stVerticalBlockBorderWrapper"]:has(.marqueur-violet) .titre-encadre { color: #d2b3ff; }
div[data-testid="stVerticalBlockBorderWrapper"]:has(.marqueur-rouge) .titre-encadre { color: #ff9b9b; }

/* ---------- badges ---------- */
.badge {
    display: inline-block;
    padding: 0.18rem 0.55rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 650;
    letter-spacing: 0.02em;
    border: 1px solid rgba(255, 255, 255, 0.12);
    background: rgba(255, 255, 255, 0.05);
    color: #c9d1d9;
    margin-right: 0.3rem;
}
.badge.bleu { border-color: rgba(76, 141, 255, 0.45); color: #9cc0ff; background: rgba(76, 141, 255, 0.10); }
.badge.vert { border-color: rgba(63, 185, 80, 0.45); color: #7ee787; background: rgba(63, 185, 80, 0.10); }
.badge.orange { border-color: rgba(240, 136, 62, 0.45); color: #ffb077; background: rgba(240, 136, 62, 0.10); }
.badge.violet { border-color: rgba(188, 140, 255, 0.45); color: #d2b3ff; background: rgba(188, 140, 255, 0.10); }

/* ---------- boutons, onglets, divers ---------- */
.stButton > button, .stDownloadButton > button {
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.14);
    font-weight: 600;
}
.stButton > button:hover {
    border-color: rgba(122, 162, 247, 0.65);
    color: #ffffff;
}
button[data-baseweb="tab"] {
    font-weight: 650;
    font-size: 0.91rem;
}
div[data-testid="stExpander"] {
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.08);
}
div[data-testid="stMetricValue"] {
    font-size: 1.6rem;
}
hr {
    border-color: rgba(255, 255, 255, 0.08);
}
.stCaption, [data-testid="stCaptionContainer"] {
    color: #96a0ae;
}
div[data-testid="stAlert"] {
    border-radius: 12px;
}

/* ---------- petits écrans ---------- */
@media (max-width: 700px) {
    .hero { padding: 1.4rem 1.2rem; }
    .hero h1 { font-size: 1.95rem; }
    .block-container { padding-top: 1.2rem; }
    .entete h1 { font-size: 1.7rem; }
}
</style>
"""


# ---------------------------------------------------------------------------
# 3. Configuration et en-têtes
# ---------------------------------------------------------------------------
def configurer_page(titre: str, icone: str = "📘", layout: str = "wide") -> None:
    """Configure la page Streamlit puis injecte la feuille de style.

    À appeler UNE SEULE FOIS, tout au début de chaque page, avant tout autre
    appel à Streamlit.
    """
    st.set_page_config(
        page_title=f"{titre} · Analyse 1",
        page_icon=icone,
        layout=layout,
        initial_sidebar_state="expanded",
    )
    injecter_css()


def injecter_css() -> None:
    """Injecte le CSS commun (thème sombre, encadrés, cartes)."""
    st.markdown(CSS, unsafe_allow_html=True)


def titre_page(titre: str, sous_titre: str, surtitre: str = "ANALYSE 1 · CP1 ENSA MARRAKECH") -> None:
    """Affiche le grand en-tête d'une page."""
    st.markdown(
        textwrap.dedent(
            f"""
            <div class="entete">
                <div class="surtitre">{surtitre}</div>
                <h1>{titre}</h1>
                <p>{sous_titre}</p>
            </div>
            """
        ).strip(),
        unsafe_allow_html=True,
    )


def badge(texte: str, couleur: str = "") -> str:
    """Renvoie le HTML d'un petit badge coloré (à insérer dans du markdown)."""
    classe = f"badge {couleur}".strip()
    return f'<span class="{classe}">{texte}</span>'


# ---------------------------------------------------------------------------
# 4. Encadrés colorés
# ---------------------------------------------------------------------------
def encadre(
    couleur: str,
    titre: str,
    texte: str | None = None,
    formules: list[str] | None = None,
    puces: list[str] | None = None,
) -> None:
    """Affiche un encadré coloré.

    Paramètres
    ----------
    couleur : "bleu" (intuition), "vert" (preuve), "orange" (erreur),
              "violet" (à retenir) ou "rouge" (alerte).
    titre   : le titre affiché en haut de l'encadré.
    texte   : un paragraphe en markdown (les maths inline s'écrivent $...$).
    formules: une liste de formules LaTeX affichées en grand.
    puces   : une liste de puces markdown.
    """
    if couleur not in COULEURS_ENCADRE:
        couleur = "bleu"
    with st.container(border=True):
        st.markdown(
            f'<span class="marqueur-{couleur}"></span>'
            f'<span class="titre-encadre">{titre}</span>',
            unsafe_allow_html=True,
        )
        if texte:
            st.markdown(texte)
        for formule in formules or []:
            st.latex(formule)
        for puce in puces or []:
            st.markdown(f"- {puce}")


# ---------------------------------------------------------------------------
# 5. Graphiques Plotly
# ---------------------------------------------------------------------------
def base_figure(
    titre: str | None = None,
    x_titre: str | None = None,
    y_titre: str | None = None,
    hauteur: int = 430,
    legende: bool = True,
) -> go.Figure:
    """Crée une figure Plotly vide avec le style de la plateforme."""
    fig = go.Figure()
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, Segoe UI, sans-serif", size=13, color="#c9d1d9"),
        margin=dict(l=10, r=10, t=58 if titre else 18, b=10),
        height=hauteur,
        hovermode="closest",
        showlegend=legende,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            x=0,
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=11.5),
        ),
    )
    if titre:
        fig.update_layout(
            title=dict(
                text=titre,
                x=0.01,
                xanchor="left",
                font=dict(size=15, color="#e6edf3"),
            )
        )
    fig.update_xaxes(
        title=x_titre,
        gridcolor="rgba(255,255,255,0.07)",
        zerolinecolor="rgba(255,255,255,0.18)",
        linecolor="rgba(255,255,255,0.15)",
    )
    fig.update_yaxes(
        title=y_titre,
        gridcolor="rgba(255,255,255,0.07)",
        zerolinecolor="rgba(255,255,255,0.18)",
        linecolor="rgba(255,255,255,0.15)",
    )
    return fig


def graphique(fig: go.Figure, note: str | None = None, hauteur: int | None = None) -> None:
    """Affiche une figure Plotly, avec éventuellement une légende sous le graphe."""
    if hauteur is not None:
        fig.update_layout(height=hauteur)
    # Streamlit a renommé use_container_width en width="stretch" dans les
    # versions récentes. On s'adapte pour éviter un avertissement de version.
    try:
        parametres = inspect.signature(st.plotly_chart).parameters
    except (TypeError, ValueError):
        parametres = {}
    if "width" in parametres:
        st.plotly_chart(
            fig,
            width="stretch",
            config={"displayModeBar": False, "scrollZoom": False},
        )
    else:
        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False, "scrollZoom": False},
        )
    if note:
        st.caption(note)


# ---------------------------------------------------------------------------
# 6. Petits composants
# ---------------------------------------------------------------------------
def carte_stat(valeur: str, libelle: str, couleur: str = BLEU) -> str:
    """Renvoie le HTML d'une carte « chiffre clé » pour l'accueil."""
    return (
        f'<div class="carte-stat">'
        f'<div class="valeur" style="color:{couleur}">{valeur}</div>'
        f'<div class="libelle">{libelle}</div>'
        f"</div>"
    )


def mini_question(question: str, reponse: str, indice: str | None = None) -> None:
    """Affiche une question dont la réponse est cachée dans un dépliant."""
    st.markdown(f"**{question}**")
    with st.expander("Voir la réponse"):
        st.markdown(reponse)
        if indice:
            st.caption(f"Indice : {indice}")


def lien_page(chemin: str, label: str) -> None:
    """Affiche un lien interne seulement si la page existe déjà.

    Cela permet à l'accueil de rester valide pendant que les pages sont
    construites une par une.
    """
    racine = Path(__file__).resolve().parent
    if (racine / chemin).exists():
        st.page_link(chemin, label=label)


def pied_page() -> None:
    """Petit pied de page discret."""
    st.markdown("---")
    st.caption(
        "Plateforme d'apprentissage **Analyse 1** · CP1 ENSA Marrakech · "
        "à travailler avec un crayon, du papier, et sans regarder la solution trop vite."
    )
