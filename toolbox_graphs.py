# -*- coding: utf-8 -*-
"""
toolbox_graphs.py — les visualisations interactives de la boîte à outils.

Chaque fonction :
  * affiche ses curseurs dans une petite colonne à droite ;
  * construit une figure Plotly ;
  * affiche la figure avec `graphique` (défini dans ui.py) ;
  * ajoute une phrase de lecture sous le graphe.

Le fichier est séparé de `pages/00_Toolbox.py` pour rester lisible :
les textes (définitions, exemples) sont dans la page, les dessins sont ici.
"""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from ui import (
    BLEU,
    GRIS,
    ORANGE,
    ROUGE,
    VERT,
    VIOLET,
    base_figure,
    graphique,
)


# ---------------------------------------------------------------------------
# 1. Limite finie : le couloir ε-δ
# ---------------------------------------------------------------------------
def g_limite() -> None:
    col_g, col_d = st.columns([2.25, 1], gap="large")
    with col_d:
        eps = st.slider("Tolérance ε sur la sortie", 0.02, 0.40, 0.15, 0.01, key="tb_lim_eps")
        delta = st.slider("Rayon δ autour de 0", 0.10, 2.50, 0.90, 0.05, key="tb_lim_delta")

    x = np.linspace(-4.0, 4.0, 4000)
    x = x[np.abs(x) > 1e-12]
    y = np.sin(x) / x

    # Plus grand δ qui marche encore : première sortie du couloir [1-ε, 1+ε].
    x_pos = x[x > 0]
    y_pos = np.sin(x_pos) / x_pos
    sorties = np.where(y_pos <= 1.0 - eps)[0]
    delta_max = float(x_pos[sorties[0]]) if len(sorties) else float("inf")

    with col_g:
        fig = base_figure("La limite en 0 de sin(x)/x vaut 1")
        fig.add_hrect(y0=1 - eps, y1=1 + eps, fillcolor=BLEU, opacity=0.14, line_width=0)
        fig.add_vrect(x0=-delta, x1=delta, fillcolor=VIOLET, opacity=0.14, line_width=0)
        fig.add_trace(
            go.Scatter(x=x, y=y, mode="lines", name="f(x) = sin(x)/x",
                       line=dict(color=BLEU, width=2.4))
        )
        mauvais = (np.abs(x) <= delta) & (np.abs(y - 1.0) >= eps)
        fig.add_trace(
            go.Scatter(x=x[mauvais], y=y[mauvais], mode="markers",
                       name="points hors du couloir",
                       marker=dict(color=ROUGE, size=6))
        )
        fig.add_hline(y=1.0, line=dict(color=VERT, width=1.6, dash="dash"))
        fig.add_vline(x=-delta, line=dict(color=VIOLET, width=1, dash="dot"))
        fig.add_vline(x=delta, line=dict(color=VIOLET, width=1, dash="dot"))
        fig.update_xaxes(range=[-4, 4])
        fig.update_yaxes(range=[-0.45, 1.35])
        graphique(fig)

    if delta <= delta_max:
        st.success(
            f"δ = {delta:.2f} convient pour ε = {eps:.2f} : aucun point rouge dans la bande violette. "
            f"Tout δ plus petit convient aussi ; le plus grand possible est ≈ {delta_max:.2f}."
        )
    else:
        st.warning(
            f"δ = {delta:.2f} est trop grand pour ε = {eps:.2f} : des points rouges sont dans la bande. "
            f"Le plus grand δ possible est ≈ {delta_max:.2f}. La limite est vraie, mais il faut choisir δ plus petit."
        )


# ---------------------------------------------------------------------------
# 2. Caractérisation séquentielle : deux chemins, deux réponses
# ---------------------------------------------------------------------------
def g_sequentielle() -> None:
    col_g, col_d = st.columns([2.25, 1], gap="large")
    with col_d:
        n = st.slider("Indice n", 0, 40, 3, 1, key="tb_seq_n")
        choix = st.radio(
            "Quelle suite ?",
            ["Suite A : f(xₙ) = 1", "Suite B : f(xₙ) = −1"],
            key="tb_seq_choix",
        )

    if choix.startswith("Suite A"):
        xn = 1.0 / (np.pi / 2 + 2 * np.pi * n)
        yn = 1.0
        nom = "xₙ = 1/(π/2 + 2πn)"
        couleur_point = ORANGE
    else:
        xn = 1.0 / (3 * np.pi / 2 + 2 * np.pi * n)
        yn = -1.0
        nom = "xₙ = 1/(3π/2 + 2πn)"
        couleur_point = VIOLET

    x = np.linspace(0.0015, 0.35, 7000)
    y = np.sin(1.0 / x)

    with col_g:
        fig = base_figure("Deux suites tendent vers 0, mais f(xₙ) ne suit pas la même piste")
        fig.add_trace(
            go.Scatter(x=x, y=y, mode="lines", name="f(x) = sin(1/x)",
                       line=dict(color=BLEU, width=1.1))
        )
        fig.add_trace(
            go.Scatter(x=[xn], y=[yn], mode="markers+text", text=[f"n = {n}"],
                       textposition="top center", name=nom,
                       marker=dict(color=couleur_point, size=13,
                                   line=dict(color="white", width=1)))
        )
        fig.add_hline(y=1, line=dict(color=ORANGE, width=1, dash="dash"))
        fig.add_hline(y=-1, line=dict(color=VIOLET, width=1, dash="dash"))
        fig.add_vline(x=0, line=dict(color=GRIS, width=1, dash="dot"))
        fig.update_xaxes(range=[0, 0.35], title="x")
        fig.update_yaxes(range=[-1.3, 1.3])
        graphique(fig)

    st.info(
        f"{nom} tend vers 0 quand n → +∞, et pourtant f(xₙ) = {yn:+.0f} pour tout n. "
        "Si f avait une limite en 0, toutes les suites tendant vers 0 donneraient la même limite. "
        "Ce n'est pas le cas : sin(1/x) n'a pas de limite en 0."
    )


# ---------------------------------------------------------------------------
# 3. Continuité : le δ rétrécit quand on approche du saut
# ---------------------------------------------------------------------------
def g_continuite() -> None:
    def marche(x: np.ndarray) -> np.ndarray:
        # x² à gauche de 1, x² + 1 à droite : un saut de hauteur 1 en 1.
        return np.where(x <= 1.0, x ** 2, x ** 2 + 1.0)

    col_g, col_d = st.columns([2.25, 1], gap="large")
    with col_d:
        x0 = st.slider("Point x₀", 0.40, 1.60, 0.90, 0.01, key="tb_cont_x0")
        eps = st.slider("Tolérance ε", 0.05, 0.80, 0.20, 0.01, key="tb_cont_eps")

    xg = np.linspace(0.2, 1.8, 5000)
    yg = marche(xg)
    y0 = float(marche(np.array([x0]))[0])
    mauvais = np.abs(yg - y0) >= eps
    delta_max = float(np.min(np.abs(xg[mauvais] - x0))) if mauvais.any() else 0.8

    with col_g:
        fig = base_figure("Continuité en x₀ : peut-on trouver un δ ?")
        fig.add_hrect(y0=y0 - eps, y1=y0 + eps, fillcolor=VERT, opacity=0.13, line_width=0)
        fig.add_vrect(x0=x0 - delta_max, x1=x0 + delta_max, fillcolor=BLEU, opacity=0.10, line_width=0)
        fig.add_trace(
            go.Scatter(x=xg, y=yg, mode="lines", name="f",
                       line=dict(color=BLEU, width=2.6))
        )
        fig.add_trace(
            go.Scatter(x=[x0], y=[y0], mode="markers", name="(x₀, f(x₀))",
                       marker=dict(color=VERT, size=12, line=dict(color="white", width=1)))
        )
        if mauvais.any():
            fig.add_trace(
                go.Scatter(x=xg[mauvais], y=yg[mauvais], mode="markers",
                           name="hors tolérance",
                           marker=dict(color=ROUGE, size=3))
            )
        fig.add_vline(x=1.0, line=dict(color=ORANGE, width=1.4, dash="dash"),
                      annotation_text="saut en 1", annotation_position="top right")
        fig.update_xaxes(range=[0.2, 1.8])
        fig.update_yaxes(range=[0, 4.3])
        graphique(fig)

    if abs(x0 - 1.0) < 1e-9:
        st.error(
            "En x₀ = 1, la fonction saute de 1 à 2. Pour ε < 0,5, aucun δ ne peut fonctionner : "
            "f n'est pas continue en 1."
        )
    else:
        st.success(
            f"Ici, δ ≈ {delta_max:.3f} convient (et tout δ plus petit aussi). "
            "Plus x₀ s'approche du saut, plus δ doit être petit : c'est exactement ce que dit la continuité."
        )


# ---------------------------------------------------------------------------
# 4. Densité de Q et de R\Q
# ---------------------------------------------------------------------------
def g_densite() -> None:
    col_g, col_d = st.columns([2.25, 1], gap="large")
    with col_d:
        n_points = st.slider("Points de chaque famille", 20, 400, 80, 20, key="tb_dens_n")
        largeur = st.slider("Largeur de la fenêtre", 0.01, 0.50, 0.20, 0.01, key="tb_dens_l")
        centre = st.slider("Centre de la fenêtre", 0.0, 1.0, 0.50, 0.01, key="tb_dens_c")

    k = np.arange(n_points + 1)
    rationnels = k / n_points
    irrationnels = (k + np.sqrt(2.0)) / n_points

    a, b = centre - largeur / 2, centre + largeur / 2
    qf = rationnels[(rationnels >= a) & (rationnels <= b)]
    irrf = irrationnels[(irrationnels >= a) & (irrationnels <= b)]

    with col_g:
        fig = base_figure("Rationnels (bleu) et irrationnels (orange) : les deux sont partout")
        fig.add_vrect(x0=a, x1=b, fillcolor="rgba(255,255,255,0.055)", line_width=0)
        fig.add_trace(
            go.Scatter(x=qf, y=np.ones_like(qf), mode="markers", name="rationnels",
                       marker=dict(color=BLEU, size=9))
        )
        fig.add_trace(
            go.Scatter(x=irrf, y=np.zeros_like(irrf), mode="markers", name="irrationnels",
                       marker=dict(color=ORANGE, size=9, symbol="diamond"))
        )
        fig.update_yaxes(range=[-0.6, 1.6], showticklabels=False, title="")
        fig.update_xaxes(range=[max(0.0, a - 0.05), min(1.0, b + 0.05)])
        fig.update_layout(height=300)
        graphique(fig)

    st.info(
        f"Dans la fenêtre ]{a:.3f} ; {b:.3f}[, il y a {len(qf)} rationnel(s) et "
        f"{len(irrf)} irrationnel(s). Réduis encore la largeur : tu en trouves toujours. "
        "C'est exactement la définition de la densité."
    )


# ---------------------------------------------------------------------------
# 5. Fonctions périodiques : deux suites, deux hauteurs
# ---------------------------------------------------------------------------
def g_periodique() -> None:
    col_g, col_d = st.columns([2.25, 1], gap="large")
    with col_d:
        periode = st.slider("Période T", 0.6, 3.0, 2.0, 0.1, key="tb_per_T")
        decalage = st.slider("Décalage a", 0.0, 3.0, 0.7, 0.05, key="tb_per_a")

    x = np.linspace(0.0, 6 * periode + 3.0, 4000)
    y = np.sin(2 * np.pi * x / periode)
    n = np.arange(0, 7)
    hauteur_a = float(np.sin(2 * np.pi * decalage / periode))

    with col_g:
        fig = base_figure("Une fonction périodique repasse par les mêmes valeurs")
        fig.add_trace(
            go.Scatter(x=x, y=y, mode="lines", name="f",
                       line=dict(color=BLEU, width=2.1))
        )
        fig.add_trace(
            go.Scatter(x=n * periode, y=np.zeros_like(n), mode="markers",
                       name="f(nT) = f(0)",
                       marker=dict(color=VERT, size=9))
        )
        fig.add_trace(
            go.Scatter(x=n * periode + decalage, y=np.full_like(n, hauteur_a),
                       mode="markers", name="f(nT + a) = f(a)",
                       marker=dict(color=ORANGE, size=9, symbol="diamond"))
        )
        for k in n[1:]:
            fig.add_vline(x=float(k * periode), line=dict(color="rgba(255,255,255,0.10)", width=1))
        fig.add_hline(y=hauteur_a, line=dict(color=ORANGE, width=1, dash="dot"))
        fig.add_hline(y=0.0, line=dict(color=VERT, width=1, dash="dot"))
        fig.update_xaxes(title="x")
        fig.update_yaxes(range=[-1.35, 1.35])
        graphique(fig)

    st.info(
        f"Les deux suites nT et nT + a tendent vers +∞. Si f avait une limite ℓ, "
        f"on aurait ℓ = f(0) = 0 et ℓ = f(a) = {hauteur_a:.3f}. "
        "Choisis a pour que f(a) ≠ 0 : la contradiction est visible."
    )


# ---------------------------------------------------------------------------
# 6. Limite monotone : le plafond attire la courbe
# ---------------------------------------------------------------------------
def g_monotone() -> None:
    col_g, col_d = st.columns([2.25, 1], gap="large")
    with col_d:
        eps = st.slider("Tolérance ε", 0.01, 0.50, 0.10, 0.01, key="tb_mono_eps")

    L = np.pi / 2
    seuil = float(np.tan(L - eps))
    xmax = max(20.0, 1.35 * seuil)
    x = np.linspace(-xmax, xmax, 5000)
    y = np.arctan(x)

    with col_g:
        fig = base_figure("Une fonction croissante majorée s'approche de son plafond")
        fig.add_hrect(y0=L - eps, y1=L, fillcolor=VERT, opacity=0.13, line_width=0)
        fig.add_hline(y=L, line=dict(color=VERT, width=1.5, dash="dash"),
                      annotation_text="L = π/2", annotation_position="top left")
        fig.add_trace(
            go.Scatter(x=x, y=y, mode="lines", name="arctan(x)",
                       line=dict(color=BLEU, width=2.5))
        )
        fig.add_vline(x=seuil, line=dict(color=ORANGE, width=1.3, dash="dot"),
                      annotation_text=f"x₀ ≈ {seuil:.2f}", annotation_position="top right")
        fig.update_xaxes(range=[-xmax, xmax])
        fig.update_yaxes(range=[-1.8, 1.8])
        graphique(fig)

    st.success(
        f"Pour tout x ≥ {seuil:.2f}, arctan(x) reste dans [L − ε, L] : "
        f"|arctan(x) − L| ≤ ε. Le seuil dépend de ε, c'est normal : "
        "plus la tolérance est petite, plus il faut aller loin."
    )


# ---------------------------------------------------------------------------
# 7. Continuité uniforme : le δ dépend-il du point ?
# ---------------------------------------------------------------------------
def g_uniforme() -> None:
    col_g, col_d = st.columns([2.25, 1], gap="large")
    with col_d:
        eps = st.slider("Tolérance ε", 0.02, 0.30, 0.10, 0.01, key="tb_uni_eps")

    x0 = np.linspace(0.01, 1.0, 600)
    # δ suffisant pour 1/x : min(x0/2, ε x0²/2).
    delta_inverse = np.minimum(x0 / 2.0, eps * x0 ** 2 / 2.0)
    # δ suffisant pour √x : ε², indépendant de x0.
    delta_racine = np.full_like(x0, eps ** 2)

    with col_g:
        fig = base_figure("Le δ nécessaire dépend-il du point ?")
        fig.add_trace(
            go.Scatter(x=x0, y=delta_inverse, mode="lines", name="1/x sur ]0, 1]",
                       line=dict(color=ORANGE, width=2.6))
        )
        fig.add_trace(
            go.Scatter(x=x0, y=delta_racine, mode="lines", name="√x sur [0, 1]",
                       line=dict(color=VERT, width=2.6))
        )
        fig.update_xaxes(title="x₀")
        fig.update_yaxes(title="δ suffisant (échelle log)", type="log")
        graphique(fig)

    st.warning(
        "Pour 1/x, la courbe orange plonge vers 0 quand x₀ → 0 : aucun δ unique ne peut "
        "marcher sur tout ]0, 1]. Pour √x, la courbe verte est plate : δ = ε² marche partout. "
        "Voilà la différence entre continue et uniformément continue."
    )


# ---------------------------------------------------------------------------
# 8. Prolongement par continuité
# ---------------------------------------------------------------------------
def g_prolongement() -> None:
    col_g, col_d = st.columns([2.25, 1], gap="large")
    with col_d:
        choix = st.radio(
            "Fonction",
            ["x sin(1/x)", "x² sin(1/x)", "sin(1/x)"],
            key="tb_prol_choix",
        )
        xmax = st.slider("Zoom sur 0 : x max", 0.01, 0.50, 0.20, 0.01, key="tb_prol_zoom")

    x = np.linspace(-xmax, xmax, 8000)
    x = x[np.abs(x) > 1e-12]

    if choix == "x sin(1/x)":
        y = x * np.sin(1.0 / x)
        enveloppe = np.abs(x)
        titre = "x sin(1/x) → 0 : le trou se bouche"
        y_range = [-1.25 * xmax, 1.25 * xmax]
    elif choix == "x² sin(1/x)":
        y = x ** 2 * np.sin(1.0 / x)
        enveloppe = x ** 2
        titre = "x² sin(1/x) → 0, et même plus vite"
        y_range = [-1.25 * xmax ** 2, 1.25 * xmax ** 2]
    else:
        y = np.sin(1.0 / x)
        enveloppe = None
        titre = "sin(1/x) : aucune limite, impossible de boucher le trou"
        y_range = [-1.35, 1.35]

    with col_g:
        fig = base_figure(titre)
        fig.add_trace(
            go.Scatter(x=x, y=y, mode="lines", name=choix,
                       line=dict(color=BLEU, width=1.5))
        )
        if enveloppe is not None:
            fig.add_trace(
                go.Scatter(x=x, y=enveloppe, mode="lines", name="enveloppe +",
                           line=dict(color=ORANGE, width=1.2, dash="dot"))
            )
            fig.add_trace(
                go.Scatter(x=x, y=-enveloppe, mode="lines", name="enveloppe −",
                           line=dict(color=ORANGE, width=1.2, dash="dot"))
            )
            fig.add_trace(
                go.Scatter(x=[0.0], y=[0.0], mode="markers", name="prolongement f(0) = 0",
                           marker=dict(color=VERT, size=13, line=dict(color="white", width=1)))
            )
        else:
            fig.add_hline(y=1.0, line=dict(color=VERT, width=1.2, dash="dash"))
            fig.add_hline(y=-1.0, line=dict(color=VERT, width=1.2, dash="dash"))
            fig.add_vline(x=0.0, line=dict(color=ROUGE, width=1.2, dash="dot"))
        fig.update_xaxes(title="x")
        fig.update_yaxes(range=y_range)
        graphique(fig)

    if enveloppe is not None:
        st.success(
            "La courbe est coincée entre les deux pointes orange, qui tendent vers 0. "
            "Par encadrement, f(x) → 0 : on pose f(0) = 0 et la fonction devient continue en 0."
        )
    else:
        st.error(
            "La courbe oscille sans cesse entre −1 et 1 au voisinage de 0. "
            "Aucune valeur en 0 ne peut rendre la fonction continue : il n'y a pas de prolongement."
        )


# ---------------------------------------------------------------------------
# 9. TVI : la ligne horizontale coupe la courbe
# ---------------------------------------------------------------------------
def g_tvi() -> None:
    col_g, col_d = st.columns([2.25, 1], gap="large")
    with col_d:
        y0 = st.slider("Hauteur y", -0.95, 2.95, 1.00, 0.05, key="tb_tvi_y")

    x = np.linspace(-2.0, 2.0, 3000)
    f = x ** 3 - 3 * x + 1

    # Solutions de f(x) = y0 : racines du polynôme x³ − 3x + (1 − y0).
    racines = np.roots([1.0, 0.0, -3.0, 1.0 - y0])
    racines = racines[np.abs(racines.imag) < 1e-8].real
    racines = np.sort(racines[(racines >= -2.0) & (racines <= 2.0)])

    with col_g:
        fig = base_figure("TVI : toute hauteur entre f(−2) et f(2) est atteinte")
        fig.add_trace(
            go.Scatter(x=x, y=f, mode="lines", name="f(x) = x³ − 3x + 1",
                       line=dict(color=BLEU, width=2.6))
        )
        fig.add_hline(y=y0, line=dict(color=ORANGE, width=1.5, dash="dash"))
        if len(racines):
            fig.add_trace(
                go.Scatter(x=racines, y=np.full_like(racines, y0), mode="markers",
                           name="solutions f(c) = y",
                           marker=dict(color=VERT, size=13, line=dict(color="white", width=1)))
            )
            for r in racines:
                fig.add_vline(x=float(r), line=dict(color=VERT, width=1, dash="dot"))
        fig.update_xaxes(title="x")
        fig.update_yaxes(title="f(x)")
        graphique(fig)

    if len(racines):
        liste = ", ".join(f"{r:.3f}" for r in racines)
        st.success(
            f"La droite horizontale coupe la courbe en {len(racines)} point(s) : c ≈ {liste}. "
            "Le TVI garantit qu'il en existe au moins un ; il ne dit pas qu'il est unique."
        )
    else:
        st.warning("Aucune solution dans [−2, 2] pour cette hauteur : elle est hors de l'intervalle des valeurs.")


# ---------------------------------------------------------------------------
# 10. Point fixe : l'escalier et la diagonale
# ---------------------------------------------------------------------------
def g_point_fixe() -> None:
    def f_pf(t: float | np.ndarray) -> float | np.ndarray:
        return 2.0 - t / 2.0

    col_g, col_d = st.columns([2.25, 1], gap="large")
    with col_d:
        u0 = st.slider("Point de départ u₀", -2.0, 5.0, 0.0, 0.1, key="tb_pf_u0")
        n_iter = st.slider("Nombre d'itérations", 1, 12, 5, 1, key="tb_pf_n")

    xs = np.linspace(-2.5, 6.5, 500)
    u = float(u0)

    with col_g:
        fig = base_figure("Point fixe : l'escalier converge vers 4/3")
        fig.add_trace(
            go.Scatter(x=xs, y=f_pf(xs), mode="lines", name="f(x) = 2 − x/2",
                       line=dict(color=BLEU, width=2.5))
        )
        fig.add_trace(
            go.Scatter(x=xs, y=xs, mode="lines", name="y = x",
                       line=dict(color=GRIS, width=1.5, dash="dash"))
        )
        fig.add_trace(
            go.Scatter(x=[u0], y=[u0], mode="markers", name="u₀",
                       marker=dict(color=ORANGE, size=10))
        )
        for _ in range(int(n_iter)):
            v = float(f_pf(u))
            fig.add_trace(go.Scatter(x=[u, u], y=[u, v], mode="lines",
                                     line=dict(color=ORANGE, width=1.2),
                                     showlegend=False, hoverinfo="skip"))
            fig.add_trace(go.Scatter(x=[u, v], y=[v, v], mode="lines",
                                     line=dict(color=ORANGE, width=1.2),
                                     showlegend=False, hoverinfo="skip"))
            u = v
        fig.add_trace(
            go.Scatter(x=[4.0 / 3.0], y=[4.0 / 3.0], mode="markers", name="point fixe 4/3",
                       marker=dict(color=VERT, size=13, line=dict(color="white", width=1)))
        )
        fig.update_xaxes(range=[-2.5, 6.5])
        fig.update_yaxes(range=[-2.2, 6.0])
        graphique(fig)

    st.info(
        f"Après {n_iter} itération(s), uₙ ≈ {u:.4f}. La suite oscille autour de 4/3 puis s'en rapproche. "
        "C'est normal : f est décroissante, donc les points alternent de part et d'autre de la diagonale."
    )


# ---------------------------------------------------------------------------
# 11. Dérivabilité : les deux pentes de la corde
# ---------------------------------------------------------------------------
def g_derivabilite() -> None:
    col_g, col_d = st.columns([2.25, 1], gap="large")
    with col_d:
        choix = st.radio("Fonction", ["|x|", "x²"], key="tb_der_choix")
        h = st.slider("h > 0", 0.05, 1.50, 0.80, 0.05, key="tb_der_h")

    x = np.linspace(-2.0, 2.0, 1200)
    f = np.abs(x) if choix == "|x|" else x ** 2
    fh = h if choix == "|x|" else h ** 2
    pente_droite = fh / h
    pente_gauche = -fh / h

    with col_g:
        fig = base_figure("Le taux d'accroissement : pente à gauche et pente à droite")
        fig.add_trace(
            go.Scatter(x=x, y=f, mode="lines", name=f"f(x) = {choix}",
                       line=dict(color=BLEU, width=2.5))
        )
        fig.add_trace(
            go.Scatter(x=[0.0, h], y=[0.0, fh], mode="lines+markers",
                       name=f"corde à droite (pente {pente_droite:.2f})",
                       line=dict(color=VERT, width=2),
                       marker=dict(size=7))
        )
        fig.add_trace(
            go.Scatter(x=[-h, 0.0], y=[fh, 0.0], mode="lines+markers",
                       name=f"corde à gauche (pente {pente_gauche:.2f})",
                       line=dict(color=ORANGE, width=2),
                       marker=dict(size=7))
        )
        fig.add_trace(
            go.Scatter(x=[0.0], y=[0.0], mode="markers", name="x₀ = 0",
                       marker=dict(color=ROUGE, size=11))
        )
        fig.update_xaxes(range=[-2, 2], title="x")
        graphique(fig)

    if choix == "|x|":
        st.error(
            f"À droite la pente vaut {pente_droite:.2f}, à gauche {pente_gauche:.2f}. "
            "Elles ne tendent pas vers la même valeur quand h → 0 : |x| n'est pas dérivable en 0."
        )
    else:
        st.success(
            f"À droite la pente vaut {pente_droite:.2f}, à gauche {pente_gauche:.2f}. "
            "Les deux tendent vers 0 quand h → 0 : f'(0) = 0. La tangente est horizontale."
        )


# ---------------------------------------------------------------------------
# 12. Dérivée et monotonie
# ---------------------------------------------------------------------------
def g_derivee_monotonie() -> None:
    from plotly.subplots import make_subplots

    col_g, col_d = st.columns([2.25, 1], gap="large")
    with col_d:
        x0 = st.slider("Point x₀", -2.40, 2.40, 0.40, 0.05, key="tb_dm_x0")

    x = np.linspace(-2.5, 2.5, 1200)
    f = x ** 3 - 3 * x
    df = 3 * x ** 2 - 3
    f0 = x0 ** 3 - 3 * x0
    d0 = 3 * x0 ** 2 - 3

    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True, row_heights=[0.62, 0.38],
        vertical_spacing=0.10,
        subplot_titles=("f(x) = x³ − 3x", "f′(x) = 3x² − 3"),
    )
    fig.add_vrect(x0=-2.5, x1=-1.0, fillcolor=VERT, opacity=0.07, line_width=0, row=1, col=1)
    fig.add_vrect(x0=1.0, x1=2.5, fillcolor=VERT, opacity=0.07, line_width=0, row=1, col=1)
    fig.add_vrect(x0=-1.0, x1=1.0, fillcolor=ROUGE, opacity=0.07, line_width=0, row=1, col=1)

    fig.add_trace(go.Scatter(x=x, y=f, mode="lines", name="f",
                             line=dict(color=BLEU, width=2.5)), row=1, col=1)
    fig.add_trace(go.Scatter(x=x, y=df, mode="lines", name="f′",
                             line=dict(color=VIOLET, width=2.2)), row=2, col=1)
    fig.add_trace(go.Scatter(x=[x0], y=[f0], mode="markers", name="x₀",
                             marker=dict(color=VERT, size=10)), row=1, col=1)
    fig.add_trace(go.Scatter(x=[x0], y=[d0], mode="markers", name="f′(x₀)",
                             marker=dict(color=VERT, size=10)), row=2, col=1)
    fig.add_vline(x=x0, line=dict(color=GRIS, width=1, dash="dot"))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#c9d1d9", size=12.5),
        height=560,
        margin=dict(l=10, r=10, t=55, b=10),
        showlegend=False,
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.07)", zerolinecolor="rgba(255,255,255,0.18)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.07)", zerolinecolor="rgba(255,255,255,0.18)")
    for annotation in fig.layout.annotations:
        annotation.font.color = "#c9d1d9"
        annotation.font.size = 13
    graphique(fig)

    if d0 > 0:
        phrase = "f′(x₀) > 0 : localement, f monte."
    elif d0 < 0:
        phrase = "f′(x₀) < 0 : localement, f descend."
    else:
        phrase = "f′(x₀) = 0 : tangente horizontale, la monotonie change de sens."
    st.info(f"f′(x₀) = {d0:+.2f}. {phrase}")


# ---------------------------------------------------------------------------
# 13. Rolle
# ---------------------------------------------------------------------------
def g_rolle() -> None:
    col_g, col_d = st.columns([2.25, 1], gap="large")
    with col_d:
        choix = st.radio(
            "Exemple",
            ["x³ − x : Rolle s'applique", "|x| : Rolle échoue"],
            key="tb_rolle_choix",
        )

    x = np.linspace(-1.1, 1.1, 1200)

    with col_g:
        if choix.startswith("x³"):
            f = x ** 3 - x
            fig = base_figure("Rolle : la tangente devient horizontale entre deux points de même hauteur")
            fig.add_trace(go.Scatter(x=x, y=f, mode="lines", name="f(x) = x³ − x",
                                     line=dict(color=BLEU, width=2.6)))
            fig.add_trace(go.Scatter(x=[-1.0, 1.0], y=[0.0, 0.0], mode="lines+markers",
                                     name="corde horizontale",
                                     line=dict(color=GRIS, width=1.5, dash="dash"),
                                     marker=dict(size=8)))
            for c in (-1.0 / np.sqrt(3.0), 1.0 / np.sqrt(3.0)):
                fc = c ** 3 - c
                fig.add_trace(go.Scatter(x=[c - 0.28, c + 0.28], y=[fc, fc], mode="lines",
                                         name="tangente horizontale",
                                         line=dict(color=ORANGE, width=2.4),
                                         showlegend=bool(c > 0)))
                fig.add_trace(go.Scatter(x=[c], y=[fc], mode="markers",
                                         marker=dict(color=VERT, size=11),
                                         showlegend=False))
            fig.update_yaxes(range=[-0.5, 0.5])
            graphique(fig)
            st.success(
                "f(−1) = f(1) = 0. Rolle garantit un c avec f′(c) = 0 ; ici il y en a même deux, "
                "c = ±1/√3. Rolle n'affirme jamais l'unicité."
            )
        else:
            f = np.abs(x)
            fig = base_figure("Rolle sans dérivabilité : le coin casse le théorème")
            fig.add_trace(go.Scatter(x=x, y=f, mode="lines", name="f(x) = |x|",
                                     line=dict(color=BLEU, width=2.6)))
            fig.add_trace(go.Scatter(x=[-1.0, 1.0], y=[1.0, 1.0], mode="lines+markers",
                                     name="corde horizontale",
                                     line=dict(color=GRIS, width=1.5, dash="dash"),
                                     marker=dict(size=8)))
            fig.add_trace(go.Scatter(x=[0.0], y=[0.0], mode="markers", name="coin en 0",
                                     marker=dict(color=ROUGE, size=12)))
            fig.update_yaxes(range=[-0.2, 1.35])
            graphique(fig)
            st.error(
                "f(−1) = f(1) = 1, mais f n'est pas dérivable en 0 : il n'existe aucun c "
                "avec f′(c) = 0. La continuité et la dérivabilité sur ]−1, 1[ sont indispensables."
            )


# ---------------------------------------------------------------------------
# 14. TAF : corde et tangente parallèle
# ---------------------------------------------------------------------------
def g_taf() -> None:
    col_g, col_d = st.columns([2.25, 1], gap="large")
    with col_d:
        a = st.slider("Point a", -3.0, 1.5, -1.0, 0.05, key="tb_taf_a")
        longueur = st.slider("Longueur b − a", 0.30, 2.50, 1.40, 0.05, key="tb_taf_l")
    b = a + longueur

    x = np.linspace(min(-3.6, a - 0.3), max(3.6, b + 0.3), 1600)
    f = np.sin(x)
    pente = (np.sin(b) - np.sin(a)) / (b - a)

    # On cherche c dans ]a, b[ tel que cos(c) = pente.
    grille = np.linspace(a + 1e-4, b - 1e-4, 6000)
    c = float(grille[np.argmin(np.abs(np.cos(grille) - pente))])
    fc = float(np.sin(c))

    with col_g:
        fig = base_figure("TAF : la pente moyenne est réalisée par une tangente")
        fig.add_trace(go.Scatter(x=x, y=f, mode="lines", name="f(x) = sin x",
                                 line=dict(color=BLEU, width=2.5)))
        fig.add_trace(go.Scatter(x=[a, b], y=[np.sin(a), np.sin(b)], mode="lines+markers",
                                 name="corde (pente moyenne)",
                                 line=dict(color=ORANGE, width=2.2),
                                 marker=dict(size=9)))
        fig.add_trace(go.Scatter(x=[c - 0.55, c + 0.55],
                                 y=[fc - pente * 0.55, fc + pente * 0.55],
                                 mode="lines", name="tangente parallèle",
                                 line=dict(color=VERT, width=2.4)))
        fig.add_trace(go.Scatter(x=[c], y=[fc], mode="markers", name="point c",
                                 marker=dict(color=VERT, size=13, line=dict(color="white", width=1))))
        fig.update_xaxes(title="x")
        fig.update_yaxes(range=[-1.5, 1.5])
        graphique(fig)

    st.latex(
        r"\frac{f(b)-f(a)}{b-a} = "
        + f"{pente:.3f}"
        + r" = f'(c) = \cos(c)"
    )
    st.info(
        f"Ici c ≈ {c:.3f}. La tangente verte est parallèle à la corde orange : "
        "c'est exactement l'égalité des accroissements finis. Le point c dépend de a et b."
    )


# ---------------------------------------------------------------------------
# 15. Dérivée n-ième de sin
# ---------------------------------------------------------------------------
def g_derivee_nieme() -> None:
    col_g, col_d = st.columns([2.25, 1], gap="large")
    with col_d:
        n = st.slider("Ordre de dérivation n", 0, 8, 1, 1, key="tb_dn_n")

    x = np.linspace(-2 * np.pi, 2 * np.pi, 1600)
    y = np.sin(x + n * np.pi / 2)

    with col_g:
        fig = base_figure(f"n = {n} : la dérivée n-ième de sin est un décalage de phase")
        fig.add_trace(go.Scatter(x=x, y=np.sin(x), mode="lines", name="sin x",
                                 line=dict(color=GRIS, width=1.2, dash="dot")))
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name=f"sin⁽{n}⁾(x)",
                                 line=dict(color=BLEU, width=2.8)))
        fig.add_trace(go.Scatter(x=[0.0], y=[float(np.sin(n * np.pi / 2))], mode="markers",
                                 name="valeur en 0",
                                 marker=dict(color=ORANGE, size=11)))
        fig.update_xaxes(title="x")
        fig.update_yaxes(range=[-1.25, 1.25], title="valeur")
        graphique(fig)

    st.latex(
        r"\sin^{(n)}(x) = \sin\left(x + \frac{n\pi}{2}\right)"
    )
    st.info(
        "Chaque dérivée ajoute π/2 à la phase : un quart de tour. "
        f"Pour n = {n}, le graphe est donc sin x décalé de {n} quart(s) de tour."
    )


# ---------------------------------------------------------------------------
# 16. Formule de Leibniz
# ---------------------------------------------------------------------------
def g_leibniz() -> None:
    col_g, col_d = st.columns([2.25, 1], gap="large")
    with col_d:
        n = st.slider("Ordre n", 0, 7, 2, 1, key="tb_leib_n")

    x = np.linspace(-2.2, 2.2, 1600)
    f = x ** 2 * np.exp(x)
    formule = np.exp(x) * (x ** 2 + 2 * n * x + n * (n - 1))
    ecart = float(np.max(np.abs(f - formule)))

    with col_g:
        fig = base_figure("Leibniz : la dérivée n-ième d'un produit n'est pas le produit des dérivées")
        fig.add_trace(go.Scatter(x=x, y=f, mode="lines", name="(x² eˣ)⁽ⁿ⁾ calculée par numpy",
                                 line=dict(color=BLEU, width=3.0)))
        fig.add_trace(go.Scatter(x=x, y=formule, mode="lines", name="formule de Leibniz",
                                 line=dict(color=ORANGE, width=2.0, dash="dash")))
        fig.update_xaxes(title="x")
        graphique(fig)

    st.latex(
        r"\left(x^2e^x\right)^{(n)} = e^x\left(x^2 + 2nx + n(n-1)\right)"
    )
    st.success(
        f"Les deux courbes se superposent : l'écart maximal calculé est {ecart:.1e}. "
        "La formule de Leibniz est donc vérifiée numériquement pour ce n."
    )


# ---------------------------------------------------------------------------
# 17. Linéarisation trigonométrique
# ---------------------------------------------------------------------------
def g_linearisation() -> None:
    col_g, col_d = st.columns([2.25, 1], gap="large")
    with col_d:
        choix = st.radio("Identité", ["sin³ x", "cos³ x"], key="tb_lin_choix")

    x = np.linspace(-np.pi, np.pi, 1400)

    with col_g:
        if choix == "sin³ x":
            gauche = np.sin(x) ** 3
            droite = (3 * np.sin(x) - np.sin(3 * x)) / 4
            composante_1 = 0.75 * np.sin(x)
            composante_2 = -0.25 * np.sin(3 * x)
            titre = "sin³ x = (3 sin x − sin 3x)/4"
            identite = r"\sin^3 x = \frac{3\sin x - \sin 3x}{4}"
        else:
            gauche = np.cos(x) ** 3
            droite = (3 * np.cos(x) + np.cos(3 * x)) / 4
            composante_1 = 0.75 * np.cos(x)
            composante_2 = 0.25 * np.cos(3 * x)
            titre = "cos³ x = (3 cos x + cos 3x)/4"
            identite = r"\cos^3 x = \frac{3\cos x + \cos 3x}{4}"

        fig = base_figure(titre)
        fig.add_trace(go.Scatter(x=x, y=composante_1, mode="lines", name="terme en x",
                                 line=dict(color=GRIS, width=1.1, dash="dot")))
        fig.add_trace(go.Scatter(x=x, y=composante_2, mode="lines", name="terme en 3x",
                                 line=dict(color=ORANGE, width=1.1, dash="dot")))
        fig.add_trace(go.Scatter(x=x, y=gauche, mode="lines", name="forme puissance",
                                 line=dict(color=BLEU, width=2.8)))
        fig.add_trace(go.Scatter(x=x, y=droite, mode="lines", name="forme linéarisée",
                                 line=dict(color=VERT, width=1.8, dash="dash")))
        fig.update_xaxes(title="x")
        fig.update_yaxes(range=[-1.35, 1.35])
        graphique(fig)

    st.latex(identite)
    st.info(
        f"L'écart maximal entre les deux formes est {np.max(np.abs(gauche - droite)):.1e} : "
        "c'est la même fonction, écrite autrement. La forme linéarisée est beaucoup plus facile à dériver n fois."
    )


# ---------------------------------------------------------------------------
# 18. Concavité : la corde est-elle au-dessus ou en dessous ?
# ---------------------------------------------------------------------------
def g_concavite() -> None:
    col_g, col_d = st.columns([2.25, 1], gap="large")
    with col_d:
        choix = st.radio(
            "Fonction",
            ["sin sur [0, π] (concave)", "x² (convexe)"],
            key="tb_conc_choix",
        )
        t1 = st.slider("Position du point A", 0.0, 0.90, 0.15, 0.05, key="tb_conc_t1")
        t2 = st.slider("Position du point B", 0.10, 1.00, 0.85, 0.05, key="tb_conc_t2")
    if t2 <= t1 + 0.03:
        t2 = min(1.0, t1 + 0.05)

    if choix.startswith("sin"):
        xa, xb = np.pi * t1, np.pi * t2
        f = np.sin
        x = np.linspace(0.0, np.pi, 1000)
        texte = "concave : la corde est sous la courbe"
    else:
        xa, xb = -1.5 + 3.0 * t1, -1.5 + 3.0 * t2
        f = lambda t: t ** 2
        x = np.linspace(-1.5, 1.5, 1000)
        texte = "convexe : la corde est au-dessus de la courbe"

    ya, yb = float(f(xa)), float(f(xb))
    y = f(x)
    corde = ya + (yb - ya) * (x - xa) / (xb - xa)
    xm = (xa + xb) / 2
    ecart = float(f(xm) - (ya + (yb - ya) * (xm - xa) / (xb - xa)))

    with col_g:
        fig = base_figure(f"{choix.split(' ')[0]} — {texte}")
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name="courbe",
                                 line=dict(color=BLEU, width=2.7)))
        fig.add_trace(go.Scatter(x=x, y=corde, mode="lines", name="corde",
                                 line=dict(color=ORANGE, width=2.0, dash="dash"),
                                 fill="tonexty", fillcolor="rgba(188,140,255,0.13)"))
        fig.add_trace(go.Scatter(x=[xa, xb], y=[ya, yb], mode="markers", name="A et B",
                                 marker=dict(color=VERT, size=10)))
        fig.add_trace(go.Scatter(x=[xm, xm], y=[float(f(xm)), float(f(xm) - ecart)],
                                 mode="lines", name="écart au milieu",
                                 line=dict(color=VIOLET, width=2.0)))
        fig.update_xaxes(title="x")
        graphique(fig)

    signe = "positive" if ecart >= 0 else "négative"
    st.info(
        f"Au milieu, l'écart entre la courbe et la corde vaut {ecart:+.3f} : il est de signe {signe}. "
        "C'est la marque de la concavité (écart ≥ 0) ou de la convexité (écart ≤ 0)."
    )


# ---------------------------------------------------------------------------
# 19. Bijection et symétrie
# ---------------------------------------------------------------------------
def g_bijection() -> None:
    col_g, col_d = st.columns([2.25, 1], gap="large")
    with col_d:
        y0 = st.slider("Sortie y₀", -0.82, 0.82, 0.60, 0.05, key="tb_bij_y0")

    x = np.linspace(-7.0, 7.0, 1600)
    f = x / (1 + np.abs(x))
    y = np.linspace(-0.96, 0.96, 1600)
    finv = y / (1 - np.abs(y))

    x0 = y0 / (1 - abs(y0))

    with col_g:
        fig = base_figure("f et sa réciproque sont symétriques par rapport à y = x")
        fig.add_trace(go.Scatter(x=x, y=f, mode="lines", name="f(x) = x/(1+|x|)",
                                 line=dict(color=BLEU, width=2.6)))
        fig.add_trace(go.Scatter(x=y, y=finv, mode="lines", name="f⁻¹(y) = y/(1−|y|)",
                                 line=dict(color=ORANGE, width=2.6)))
        fig.add_trace(go.Scatter(x=x, y=x, mode="lines", name="y = x",
                                 line=dict(color=GRIS, width=1.4, dash="dash")))
        fig.add_trace(go.Scatter(x=[x0], y=[y0], mode="markers", name="(x₀, y₀) sur f",
                                 marker=dict(color=VERT, size=12)))
        fig.add_trace(go.Scatter(x=[y0], y=[x0], mode="markers", name="point symétrique",
                                 marker=dict(color=VIOLET, size=12)))
        fig.update_xaxes(range=[-5.5, 5.5], title="x")
        fig.update_yaxes(range=[-5.5, 5.5], title="y")
        graphique(fig)

    st.latex(rf"f\left({x0:.3f}\right) = {y0:.2f} \quad\text{{et}}\quad f^{{-1}}({y0:.2f}) = {x0:.3f}")
    st.info(
        "La courbe orange est l'image de la bleue par le miroir y = x. "
        "C'est la signature d'une fonction réciproque."
    )


# ---------------------------------------------------------------------------
# 20. Dérivable mais pas C¹
# ---------------------------------------------------------------------------
def g_c1() -> None:
    from plotly.subplots import make_subplots

    col_g, col_d = st.columns([2.25, 1], gap="large")
    with col_d:
        xmax = st.slider("Zoom : x max", 0.02, 1.00, 0.25, 0.01, key="tb_c1_zoom")

    x = np.linspace(-xmax, xmax, 12000)
    x = x[np.abs(x) > 1e-12]
    f = x ** 2 * np.sin(1.0 / x)
    df = 2 * x * np.sin(1.0 / x) - np.cos(1.0 / x)

    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True, row_heights=[0.44, 0.56],
        vertical_spacing=0.10,
        subplot_titles=("f(x) = x² sin(1/x), prolongée par f(0) = 0",
                        "f′(x) = 2x sin(1/x) − cos(1/x) : elle oscille sans limite"),
    )
    fig.add_trace(go.Scatter(x=x, y=f, mode="lines", name="f",
                             line=dict(color=BLEU, width=2.2)), row=1, col=1)
    fig.add_trace(go.Scatter(x=[0.0], y=[0.0], mode="markers", name="f(0) = 0",
                             marker=dict(color=VERT, size=11)), row=1, col=1)
    fig.add_trace(go.Scatter(x=x, y=df, mode="lines", name="f′",
                             line=dict(color=ORANGE, width=1.2)), row=2, col=1)
    fig.add_trace(go.Scatter(x=[0.0], y=[0.0], mode="markers", name="f′(0) = 0",
                             marker=dict(color=VERT, size=11)), row=2, col=1)
    fig.add_hline(y=1.0, line=dict(color=GRIS, width=1, dash="dot"), row=2, col=1)
    fig.add_hline(y=-1.0, line=dict(color=GRIS, width=1, dash="dot"), row=2, col=1)

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#c9d1d9", size=12.5),
        height=580,
        margin=dict(l=10, r=10, t=55, b=10),
        showlegend=False,
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.07)", zerolinecolor="rgba(255,255,255,0.18)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.07)", zerolinecolor="rgba(255,255,255,0.18)")
    for annotation in fig.layout.annotations:
        annotation.font.color = "#c9d1d9"
        annotation.font.size = 12.5
    graphique(fig)

    st.warning(
        "En bas, la dérivée passe sans arrêt de valeurs proches de −1 à des valeurs proches de +1. "
        "Elle n'a pas de limite en 0 : f est dérivable partout, mais f′ n'est pas continue en 0. "
        "Autrement dit, f n'est pas de classe C¹ sur R."
    )
