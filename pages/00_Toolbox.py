# -*- coding: utf-8 -*-
"""
00_Toolbox.py — la boîte à outils de l'analyse.

Cette page contient les 20 notions utilisées dans le TD 3. Pour chacune :
  * l'énoncé formel (en violet : c'est la référence à retenir) ;
  * la version « en mots simples » (en bleu : l'intuition) ;
  * une visualisation interactive ;
  * un exemple (en vert) et un contre-exemple (en orange) ;
  * l'idée de la preuve ;
  * « quand l'utiliser ? » et les exercices du TD concernés.

Les graphiques sont dans toolbox_graphs.py : la page reste lisible.
"""

from __future__ import annotations

import sys
import textwrap
import unicodedata
from pathlib import Path

# On ajoute la racine du projet au chemin d'import : ainsi `import ui` et
# `import toolbox_graphs` fonctionnent même quand Streamlit exécute la page
# depuis le dossier pages/.
RACINE = Path(__file__).resolve().parents[1]
if str(RACINE) not in sys.path:
    sys.path.insert(0, str(RACINE))

import streamlit as st  # noqa: E402

from ui import badge, configurer_page, encadre, pied_page, titre_page  # noqa: E402
from toolbox_graphs import (  # noqa: E402
    g_bijection,
    g_c1,
    g_concavite,
    g_continuite,
    g_densite,
    g_derivabilite,
    g_derivee_monotonie,
    g_derivee_nieme,
    g_leibniz,
    g_limite,
    g_linearisation,
    g_monotone,
    g_periodique,
    g_point_fixe,
    g_prolongement,
    g_rolle,
    g_sequentielle,
    g_taf,
    g_tvi,
    g_uniforme,
)

configurer_page("Boîte à outils", "🧰")


# ---------------------------------------------------------------------------
# 1. Les 20 notions
# ---------------------------------------------------------------------------
NOTIONS = [
    # ------------------------------------------------------------------ 1
    {
        "id": "limite",
        "famille": "Limites",
        "titre": "Limite finie en un point",
        "enonce": r"""
Soit $f:D\to\mathbb{R}$, soit $x_0$ un point **adhérent** à $D$ (on peut s'approcher de $x_0$ par des points de $D$), et soit $\ell\in\mathbb{R}$.

On dit que $f$ tend vers $\ell$ quand $x$ tend vers $x_0$, et on note $\displaystyle\lim_{x\to x_0}f(x)=\ell$, si :

$$ \forall\,\varepsilon>0,\quad \exists\,\delta>0,\quad \forall x\in D,\qquad 0<|x-x_0|<\delta\ \Longrightarrow\ |f(x)-\ell|\le\varepsilon. $$

La même idée définit la limite en $+\infty$ : pour tout $\varepsilon>0$, il existe $A$ tel que $x\ge A\Rightarrow|f(x)-\ell|\le\varepsilon$ (et symétriquement en $-\infty$).
""",
        "mots": r"""
On te donne une tolérance $\varepsilon$ sur la **sortie**. Tu dois répondre par un rayon $\delta$ autour de $x_0$ tel que tous les $x$ de ce rayon, **différents de $x_0$**, aient leur image dans le couloir $[\ell-\varepsilon,\ell+\varepsilon]$.

L'ordre est essentiel : $\varepsilon$ est choisi d'abord (par l'adversaire), $\delta$ est ta réponse. Un bon $\delta$ doit exister pour **tous** les $\varepsilon>0$, même minuscules. Si un $\delta$ marche, tous les plus petits marchent aussi.
""",
        "preuve": r"""
On fixe $\varepsilon>0$. On cherche $\delta>0$ qui rend l'implication vraie. Pour $f(x)=2x+1$ en $x_0=1$, on calcule $|f(x)-3|=2|x-1|$ : il suffit donc de prendre $\delta=\varepsilon/2$.

La preuve d'une limite est toujours la même histoire : on part de $|f(x)-\ell|$, on le majore par une expression en $|x-x_0|$, puis on choisit $\delta$ pour que cette expression soit $<\varepsilon$.
""",
        "exemple": r"""
$f(x)=2x+1$ en $x_0=1$ : la limite vaut $3$. En effet, pour $\delta=\varepsilon/2$,
$$ |x-1|<\delta\ \Longrightarrow\ |f(x)-3|=2|x-1|<2\delta=\varepsilon. $$
""",
        "contre": r"""
La fonction échelon $f(x)=0$ si $x<0$, $f(x)=1$ si $x\ge0$, n'a **pas** de limite en $0$ : la limite à gauche (quand $x\to0$ avec $x<0$) vaut $0$, la limite à droite (quand $x\to0$ avec $x>0$) vaut $1$. Avec $\varepsilon=\tfrac12$, aucun $\delta$ ne peut rendre les deux côtés compatibles.
""",
        "quand": r"""
Pour traduire rigoureusement « $f(x)$ devient proche de $\ell$ », pour prouver une limite par encadrement, ou pour montrer qu'une limite **n'existe pas** (en exhibant deux comportements incompatibles).
""",
        "td": "Exercice 1 · Exercice 7",
        "graph": g_limite,
    },
    # ------------------------------------------------------------------ 2
    {
        "id": "sequentielle",
        "famille": "Limites",
        "titre": "Caractérisation séquentielle",
        "enonce": r"""
Soit $f:D\to\mathbb{R}$, $x_0$ adhérent à $D$ et $\ell\in\mathbb{R}$. Alors :
$$ \lim_{x\to x_0}f(x)=\ell \iff \text{pour toute suite } (x_n)\subset D \text{ avec } x_n\to x_0 \text{ et } x_n\neq x_0,\quad f(x_n)\to\ell. $$
""",
        "mots": r"""
Une fonction a une limite si **tous les chemins** qui s'approchent de $x_0$ donnent la même hauteur. Si tu trouves deux suites qui tendent vers $x_0$ mais dont les images tendent vers deux valeurs différentes, la limite n'existe pas.

C'est l'outil le plus rapide pour **démontrer une non-continuité** : deux suites suffisent.
""",
        "preuve": r"""
**Sens direct.** Si $f(x)\to\ell$, prenons $\varepsilon>0$ et le $\delta$ de la définition. Comme $x_n\to x_0$, pour $n$ assez grand on a $|x_n-x_0|<\delta$, donc $|f(x_n)-\ell|\le\varepsilon$. C'est bien $f(x_n)\to\ell$.

**Réciproque (par contraposée).** Si $f$ ne tend pas vers $\ell$, il existe $\varepsilon>0$ tel que **tout** $\delta>0$ échoue. En prenant $\delta=1/n$, on fabrique $x_n$ avec $0<|x_n-x_0|<1/n$ et $|f(x_n)-\ell|\ge\varepsilon$. Cette suite tend vers $x_0$ mais $f(x_n)$ ne tend pas vers $\ell$ : contradiction.
""",
        "exemple": r"""
$f(x)=x^2$ en $x_0=1$ : pour $x_n=1+\frac1n$, on a $f(x_n)\to1=f(1)$. Toutes les suites donnent la même réponse.
""",
        "contre": r"""
$f(x)=\sin(1/x)$ en $0$. La suite $a_n=\dfrac{1}{\pi/2+2\pi n}$ tend vers $0$ et $f(a_n)=1$. La suite $b_n=\dfrac{1}{3\pi/2+2\pi n}$ tend aussi vers $0$ et $f(b_n)=-1$. Deux limites différentes : pas de limite en $0$.
""",
        "quand": r"""
Pour montrer qu'une fonction n'a pas de limite ou n'est pas continue (deux suites), et pour transporter les théorèmes sur les suites vers les fonctions.
""",
        "td": "Exercice 1 · Exercice 2",
        "graph": g_sequentielle,
    },
    # ------------------------------------------------------------------ 3
    {
        "id": "continuite",
        "famille": "Limites",
        "titre": "Continuité",
        "enonce": r"""
$f$ est **continue en** $x_0\in D$ si
$$ \forall\,\varepsilon>0,\quad \exists\,\delta>0,\quad \forall x\in D,\qquad |x-x_0|<\delta\ \Longrightarrow\ |f(x)-f(x_0)|<\varepsilon. $$
C'est la définition de la limite avec $\ell=f(x_0)$.

$f$ est **continue sur** $I$ si elle est continue en tout point de $I$.

Les sommes, produits, quotients (dénominateur non nul) et composées de fonctions continues sont continus. Les polynômes, $\exp$, $\ln$, $\sin$, $\cos$, $\tan$, $|\cdot|$ et $\sqrt{\cdot}$ sont continus sur leur domaine.
""",
        "mots": r"""
Un petit déplacement en $x$ ne provoque qu'un petit déplacement en $f$. On dit souvent « la courbe se dessine sans lever le crayon » : c'est une bonne image, mais ce n'est **pas** une preuve. La preuve, c'est le $\varepsilon$-$\delta$.
""",
        "preuve": r"""
C'est la même démonstration que pour les limites, avec $\ell=f(x_0)$.

Pour composer deux fonctions continues, on emboîte deux $\varepsilon$-$\delta$ : la continuité de $g$ en $f(x_0)$ fournit un premier rayon, puis la continuité de $f$ en $x_0$ fournit le rayon final.
""",
        "exemple": r"""
$f(x)=x^2$ est continue partout. En $x_0$, $|x^2-x_0^2|=|x-x_0|\,|x+x_0|$ ; en restant près de $x_0$, le facteur $|x+x_0|$ est borné, et le produit tend vers $0$.

$\sqrt{x}$ est continue sur $[0,+\infty[$ (continuité à droite en $0$).
""",
        "contre": r"""
La fonction échelon $f(x)=0$ si $x<0$, $f(x)=1$ si $x\ge0$, est discontinue en $0$ : elle saute de $0$ à $1$.

Attention : $f(x)=\sin(1/x)$ n'est même pas prolongeable par continuité en $0$ (voir la notion « prolongement »).
""",
        "quand": r"""
Dès qu'on veut appliquer le TVI, parler d'image d'un intervalle, d'extrema sur un segment, ou prolonger une fonction.
""",
        "td": "Exercice 1 · Exercice 3 · Exercice 4",
        "graph": g_continuite,
    },
    # ------------------------------------------------------------------ 4
    {
        "id": "densite",
        "famille": "Limites",
        "titre": "Densité de Q et de R\\Q dans R",
        "enonce": r"""
$\mathbb{Q}$ et $\mathbb{R}\setminus\mathbb{Q}$ sont **denses** dans $\mathbb{R}$ :
$$ \forall a<b,\qquad ]a,b[\cap\mathbb{Q}\neq\varnothing \quad\text{et}\quad ]a,b[\cap(\mathbb{R}\setminus\mathbb{Q})\neq\varnothing. $$
Autrement dit : tout intervalle ouvert non vide contient au moins un rationnel et au moins un irrationnel.
""",
        "mots": r"""
Entre deux réels, aussi proches soient-ils, il y a toujours un rationnel **et** un irrationnel. Les deux familles sont partout : aucun intervalle, même minuscule, n'est vide de l'une ou de l'autre.

C'est ce qui permet, dans l'exercice 1, de trouver des suites de rationnels et des suites d'irrationnels qui convergent vers n'importe quel $x_0$.
""",
        "preuve": r"""
**Pour un rationnel.** On choisit $n\in\mathbb{N}^*$ assez grand pour que $\frac1n<b-a$. Les nombres $\frac{k}{n}$ sont espacés de $\frac1n$ : l'un d'eux tombe forcément dans $]a,b[$.

**Pour un irrationnel.** On prend un rationnel $q\in]a,b[$ (on vient de le prouver), puis on ajoute $\frac{\sqrt2}{N}$ avec $N$ assez grand pour rester dans $]a,b[$. Le nombre $q+\frac{\sqrt2}{N}$ est irrationnel, car $\sqrt2$ l'est.
""",
        "exemple": r"""
Dans $]1\,;\,1{,}001[$, le nombre $1{,}0005$ est rationnel, et $1+\frac{\sqrt2}{10000}$ est irrationnel. Les deux sont dans l'intervalle.
""",
        "contre": r"""
$\mathbb{Z}$ n'est **pas** dense dans $\mathbb{R}$ : l'intervalle $]0{,}5\,;\,0{,}6[$ ne contient aucun entier.

De même, l'ensemble $\{0\}$ n'est pas dense : l'intervalle $]0{,}1\,;\,0{,}2[$ ne le rencontre pas.
""",
        "quand": r"""
Pour construire des suites de rationnels ou d'irrationnels, pour étendre une propriété vraie sur $\mathbb{Q}$ à tout $\mathbb{R}$ par continuité, et pour l'exercice 1.
""",
        "td": "Exercice 1 · Exercice 3",
        "graph": g_densite,
    },
    # ------------------------------------------------------------------ 5
    {
        "id": "periodique",
        "famille": "Limites",
        "titre": "Fonctions périodiques",
        "enonce": r"""
Soit $T>0$. Une fonction $f:\mathbb{R}\to\mathbb{R}$ est **$T$-périodique** si
$$ \forall x\in\mathbb{R},\qquad f(x+T)=f(x). $$

Si $f$ est périodique (de période $T>0$) et admet une limite **finie** en $+\infty$, alors $f$ est constante.
""",
        "mots": r"""
La fonction se répète identique à elle-même tous les $T$. À l'infini, elle repasse sans cesse par les mêmes valeurs. Une limite, elle, oblige la fonction à finir par rester dans un petit couloir. Les deux sont incompatibles si la fonction n'est pas constante.

Conséquence : une fonction périodique **non constante** n'a pas de limite en $+\infty$.
""",
        "preuve": r"""
Supposons que $f$ ait une limite finie $\ell$ en $+\infty$.

Pour tout $n\in\mathbb{N}$, $nT\to+\infty$ et $f(nT)=f(0)$, donc $\ell=f(0)$.

Pour tout réel $a$, $nT+a\to+\infty$ et $f(nT+a)=f(a)$, donc $\ell=f(a)$.

Ainsi $f(a)=f(0)$ pour tout $a$ : $f$ est constante.
""",
        "exemple": r"""
$\sin$ et $\cos$ sont $2\pi$-périodiques. La fonction « partie fractionnaire » $x\mapsto x-\lfloor x\rfloor$ est $1$-périodique.

Aucune de ces fonctions non constantes n'a de limite en $+\infty$.
""",
        "contre": r"""
$f(x)=x\sin x$ n'est pas périodique et n'a pas de limite en $+\infty$ : les deux propriétés peuvent échouer ensemble.

Une fonction **constante** est périodique (de toute période $T>0$) et a une limite : c'est pour cela que le théorème parle de fonction **non constante**.
""",
        "quand": r"""
Pour montrer qu'une limite en $+\infty$ n'existe pas : on choisit deux suites $nT$ et $nT+a$ qui donnent deux valeurs différentes.
""",
        "td": "Exercice 2.1",
        "graph": g_periodique,
    },
    # ------------------------------------------------------------------ 6
    {
        "id": "monotone",
        "famille": "Limites",
        "titre": "Fonctions monotones et limite monotone",
        "enonce": r"""
Soit $f:\mathbb{R}\to\mathbb{R}$ croissante et majorée. Alors
$$ \lim_{x\to+\infty}f(x)=\sup_{x\in\mathbb{R}}f(x)\in\mathbb{R}. $$

Si $f$ est croissante et **non majorée**, alors $\displaystyle\lim_{x\to+\infty}f(x)=+\infty$.

Énoncés analogues pour une fonction décroissante : limite égale à $\inf f$ si elle est minorée, à $-\infty$ sinon.
""",
        "mots": r"""
La fonction monte, mais bute sur un plafond fini. Elle finit par s'approcher de ce plafond sans le dépasser : c'est la définition même de la limite.

C'est un théorème d'**existence** : on ne calcule pas la limite, on prouve qu'elle existe et on l'identifie au plafond.
""",
        "preuve": r"""
Soit $L=\sup_{x\in\mathbb{R}}f(x)$, qui est fini car $f$ est majorée.

Soit $\varepsilon>0$. Par définition du sup, il existe $x_0$ tel que $f(x_0)>L-\varepsilon$.

Pour tout $x\ge x_0$, la croissance donne $f(x_0)\le f(x)\le L$. Donc $f(x)\in[L-\varepsilon,L]$, c'est-à-dire $|f(x)-L|\le\varepsilon$. C'est exactement la limite.
""",
        "exemple": r"""
$\arctan$ est croissante et majorée par $\frac\pi2$ : sa limite en $+\infty$ est $\frac\pi2$.

$f(x)=1-e^{-x}$ est croissante et majorée par $1$ : sa limite est $1$.
""",
        "contre": r"""
$f(x)=x$ est croissante mais non majorée : sa limite est $+\infty$, pas un réel fini.

$f(x)=\sin x$ n'est pas monotone : le théorème ne s'applique pas, et la limite n'existe pas.
""",
        "quand": r"""
Pour prouver l'existence d'une limite sans calcul (exercice 2.2), pour étudier une suite monotone, ou pour encadrer une fonction.
""",
        "td": "Exercice 2.2 · Exercice 2.3",
        "graph": g_monotone,
    },
    # ------------------------------------------------------------------ 7
    {
        "id": "uniforme",
        "famille": "Continuité",
        "titre": "Continuité uniforme et théorème de Heine",
        "enonce": r"""
$f:D\to\mathbb{R}$ est **uniformément continue** sur $D$ si
$$ \forall\,\varepsilon>0,\quad \exists\,\delta>0,\quad \forall x,y\in D,\qquad |x-y|<\delta\ \Longrightarrow\ |f(x)-f(y)|<\varepsilon. $$

Le $\delta$ ne dépend que de $\varepsilon$, **pas** du point $x$.

**Théorème de Heine.** Si $f$ est continue sur un segment $[a,b]$, alors $f$ est uniformément continue sur $[a,b]$.
""",
        "mots": r"""
Continuité simple : en chaque point, on peut choisir un rayon adapté. Continuité uniforme : un **seul** rayon marche partout, du même coup pour tous les points.

Sur un segment (fermé et borné), il n'y a pas de bord infini ni de trou : la continuité simple suffit à fabriquer un $\delta$ global. C'est Heine.
""",
        "preuve": r"""
**Heine, par l'absurde.** Supposons $f$ non uniformément continue sur $[a,b]$. Il existe $\varepsilon>0$ tel que, pour tout $n$, on trouve $x_n,y_n\in[a,b]$ avec
$$ |x_n-y_n|<\frac1n \quad\text{et}\quad |f(x_n)-f(y_n)|\ge\varepsilon. $$

La suite $(x_n)$ est bornée : le théorème de Bolzano–Weierstrass permet d'en extraire une sous-suite $x_{\varphi(n)}\to c\in[a,b]$. Comme $|x_{\varphi(n)}-y_{\varphi(n)}|\to0$, on a aussi $y_{\varphi(n)}\to c$. La continuité de $f$ en $c$ donne alors $|f(x_{\varphi(n)})-f(y_{\varphi(n)})|\to0$, ce qui contredit l'inégalité $\ge\varepsilon$.
""",
        "exemple": r"""
$\sqrt{x}$ est uniformément continue sur $[0,1]$ : on peut prendre $\delta=\varepsilon^2$, car
$$ |\sqrt{x}-\sqrt{y}|\le\sqrt{|x-y|}. $$

Toute fonction **lipschitzienne** ($|f(x)-f(y)|\le M|x-y|$) est uniformément continue : $\delta=\varepsilon/M$ marche.
""",
        "contre": r"""
$f(x)=1/x$ est continue sur $]0,1]$ mais **pas** uniformément continue : avec $x_n=\frac1n$ et $y_n=\frac1{n+1}$, on a $x_n-y_n\to0$ et pourtant $f(x_n)-f(y_n)=-1$.

$x^2$ est continue sur $\mathbb{R}$ mais pas uniformément continue : le $\delta$ nécessaire grandit avec $|x|$.
""",
        "quand": r"""
Pour faire passer une limite sous le signe $f$ (exercice 6), pour majorer $|f(x_n)-f(y_n)|$ quand $x_n-y_n\to0$, ou pour remplacer un $\delta$ dépendant du point par un $\delta$ global.
""",
        "td": "Exercice 6",
        "graph": g_uniforme,
    },
    # ------------------------------------------------------------------ 8
    {
        "id": "prolongement",
        "famille": "Continuité",
        "titre": "Prolongement par continuité",
        "enonce": r"""
Soit $f:D\to\mathbb{R}$ et soit $a\notin D$ adhérent à $D$.

On dit que $f$ **se prolonge par continuité** en $a$ s'il existe $\ell\in\mathbb{R}$ tel que
$$ \lim_{x\to a}f(x)=\ell. $$

On pose alors $\widetilde f(a)=\ell$ et $\widetilde f(x)=f(x)$ pour $x\in D$. La fonction $\widetilde f$ est continue en $a$.
""",
        "mots": r"""
La courbe a un trou en $a$. Si, en s'approchant de $a$, elle vise une hauteur précise $\ell$, on remplit le trou avec cette hauteur. La fonction prolongée est continue.

Si la courbe oscille ou part à l'infini, aucun remplissage ne peut rendre la fonction continue.
""",
        "preuve": r"""
Il suffit de poser $f(a)=\ell$. Pour $x\neq a$, $|f(x)-f(a)|=|f(x)-\ell|$, qui est $<\varepsilon$ dès que $|x-a|<\delta$ par définition de la limite. C'est exactement la continuité en $a$.

Hors de $a$, la fonction n'a pas changé : elle reste continue là où elle l'était.
""",
        "exemple": r"""
$f(x)=x\sin(1/x)$ sur $\mathbb{R}^*$ se prolonge en $0$ par $f(0)=0$, car $|x\sin(1/x)|\le|x|\to0$.

$f(x)=\frac{\sin x}{x}$ se prolonge en $0$ par $f(0)=1$.
""",
        "contre": r"""
$f(x)=\sin(1/x)$ n'a pas de limite en $0$ : pas de prolongement par continuité.

$f(x)=1/x$ n'a pas de limite **finie** en $0$ : pas de prolongement par continuité non plus (la limite est infinie).
""",
        "quand": r"""
Pour boucher une singularité apparente (exercice 7), pour définir proprement $f(0)$, ou pour étudier la dérivabilité après prolongement.
""",
        "td": "Exercice 7",
        "graph": g_prolongement,
    },
    # ------------------------------------------------------------------ 9
    {
        "id": "tvi",
        "famille": "Continuité",
        "titre": "Théorème des valeurs intermédiaires (TVI)",
        "enonce": r"""
Soit $f:[a,b]\to\mathbb{R}$ continue. Pour tout $y$ compris entre $f(a)$ et $f(b)$ (au sens large), il existe $c\in[a,b]$ tel que
$$ f(c)=y. $$

En particulier, si $f(a)f(b)<0$, il existe $c\in]a,b[$ tel que $f(c)=0$.
""",
        "mots": r"""
Pour aller de la hauteur $f(a)$ à la hauteur $f(b)$, la courbe doit traverser **toutes** les hauteurs intermédiaires. Elle ne peut pas sauter.

C'est le théorème qui prouve l'existence d'une solution à une équation $f(x)=y$, même quand on ne sait pas la calculer.
""",
        "preuve": r"""
On suppose $f(a)<y<f(b)$ (les autres cas se traitent de la même façon).

On pose $A=\{x\in[a,b] : f(x)\le y\}$. Cet ensemble est majoré par $b$ et **non vide** : comme $f(a)<y$, la continuité de $f$ en $a$ donne $f(x)<y$ pour $x$ juste à droite de $a$. Donc $c=\sup A$ existe et $c>a$.

Par continuité et par la définition du sup, on montre que $f(c)\le y$. Si on avait $f(c)<y$, la continuité donnerait $f<y$ sur un petit intervalle à droite de $c$, donc des points de $A$ plus grands que $c$, ce qui contredit $c=\sup A$ (si $c=b$, on contredit directement $f(b)>y$). Ainsi $f(c)=y$.
""",
        "exemple": r"""
L'équation $\cos x=x$ a une solution dans $[0,1]$ : $f(x)=\cos x-x$ est continue, $f(0)=1>0$ et $f(1)=\cos1-1<0$.

L'équation $x^3-3x+1=0$ a trois solutions réelles, que l'on peut encadrer par le TVI.
""",
        "contre": r"""
La fonction échelon (discontinue en $0$) passe de $0$ à $1$ sans prendre la valeur $\tfrac12$ : la continuité est indispensable.

$\frac1x$ sur $[-1,1]$ n'est pas définie en $0$ : on ne peut pas appliquer le TVI sur un intervalle qui contient un trou.
""",
        "quand": r"""
Pour prouver l'existence d'une solution (exercices 4.1 à 4.3), pour le point fixe (exercice 2.3), et pour fabriquer des fonctions auxiliaires.
""",
        "td": "Exercices 4.1 à 4.4 · Exercice 2.3",
        "graph": g_tvi,
    },
    # ------------------------------------------------------------------ 10
    {
        "id": "point_fixe",
        "famille": "Continuité",
        "titre": "Point fixe",
        "enonce": r"""
Un **point fixe** de $f$ est un réel $x$ tel que
$$ f(x)=x. $$

**Théorème 1.** Si $f:[a,b]\to[a,b]$ est continue, alors $f$ admet au moins un point fixe.

**Théorème 2.** Si $f:\mathbb{R}\to\mathbb{R}$ est continue et décroissante, alors $f$ admet un **unique** point fixe.
""",
        "mots": r"""
Un point fixe, c'est un endroit où la courbe rencontre la diagonale $y=x$ : l'entrée égale la sortie.

Théorème 1 : si $f$ envoie un segment dans lui-même, elle est obligée de croiser la diagonale. Théorème 2 : une fonction décroissante ne peut croiser la diagonale qu'une seule fois, parce que $f(x)-x$ est strictement décroissante.
""",
        "preuve": r"""
**Théorème 1.** On pose $g(x)=f(x)-x$. Comme $f(a)\in[a,b]$, $g(a)=f(a)-a\ge0$. Comme $f(b)\in[a,b]$, $g(b)=f(b)-b\le0$. La fonction $g$ est continue, donc le TVI donne $c$ avec $g(c)=0$, c'est-à-dire $f(c)=c$.

**Théorème 2.** Pour l'existence, $g=f-\mathrm{id}$ est continue, $g(x)\le f(0)-x\to-\infty$ quand $x\to+\infty$ et $g(x)\ge f(0)-x\to+\infty$ quand $x\to-\infty$ : le TVI donne un zéro. Pour l'unicité, si $x<y$, alors $f(x)\ge f(y)$, donc
$$ g(x)=f(x)-x>f(y)-y=g(y). $$
$g$ est strictement décroissante : elle ne peut s'annuler qu'une fois.
""",
        "exemple": r"""
$f(x)=2-\frac x2$ est continue et décroissante sur $\mathbb{R}$. Son point fixe vérifie $x=2-\frac x2$, donc $\frac{3x}{2}=2$ et $x=\frac43$.

$f(x)=\sqrt{x}$ envoie $[0,1]$ dans $[0,1]$ ; ses points fixes sont $0$ et $1$ : sans décroissance stricte, l'unicité peut échouer.
""",
        "contre": r"""
$f(x)=x+1$ n'a aucun point fixe : $f(x)-x=1$ ne s'annule jamais.

$f(x)=x^2$ sur $\mathbb{R}$ a deux points fixes, $0$ et $1$ : la croissance ne donne pas l'unicité.
""",
        "quand": r"""
Pour l'exercice 2.3, pour étudier une suite $u_{n+1}=f(u_n)$, ou pour transformer une équation en recherche de point fixe.
""",
        "td": "Exercice 2.3",
        "graph": g_point_fixe,
    },
    # ------------------------------------------------------------------ 11
    {
        "id": "derivabilite",
        "famille": "Dérivation",
        "titre": "Dérivabilité",
        "enonce": r"""
$f$ est **dérivable en** $x_0$ si la limite suivante existe et est finie :
$$ f'(x_0)=\lim_{h\to0}\frac{f(x_0+h)-f(x_0)}{h}. $$

$f$ est dérivable sur $I$ si elle l'est en tout point de $I$.

**Dérivable implique continu** : si $f$ est dérivable en $x_0$, alors $f$ est continue en $x_0$.
""",
        "mots": r"""
Le taux d'accroissement est la pente de la corde entre $x_0$ et $x_0+h$. Si cette pente se stabilise quand $h\to0$, la corde devient la tangente, et cette pente limite est $f'(x_0)$.

La réciproque est fausse : une fonction peut être continue sans avoir de tangente (par exemple $|x|$ en $0$).
""",
        "preuve": r"""
**Dérivable $\Rightarrow$ continue.** Si le taux $\frac{f(x_0+h)-f(x_0)}{h}$ tend vers $f'(x_0)$, alors
$$ f(x_0+h)-f(x_0)=h\cdot\frac{f(x_0+h)-f(x_0)}{h}\longrightarrow 0\times f'(x_0)=0. $$
Donc $f(x_0+h)\to f(x_0)$ : $f$ est continue en $x_0$.
""",
        "exemple": r"""
$f(x)=x^2$ est dérivable partout, $f'(x)=2x$.

$f(x)=x^2\sin(1/x)$ prolongée par $f(0)=0$ est dérivable en $0$, car
$$ \frac{f(h)-f(0)}{h}=h\sin(1/h)\longrightarrow0. $$
""",
        "contre": r"""
$f(x)=|x|$ n'est pas dérivable en $0$ : le taux vaut $1$ à droite et $-1$ à gauche.

$f(x)=\sqrt{x}$ n'est pas dérivable en $0$ : le taux vaut $\frac{1}{\sqrt h}\to+\infty$ (tangente verticale).
""",
        "quand": r"""
Pour calculer une dérivée, pour appliquer Rolle ou le TAF (exercices 4, 9, 10), et pour étudier le prolongement d'une fonction (exercice 7).
""",
        "td": "Exercice 7 · Exercices 8, 9, 10",
        "graph": g_derivabilite,
    },
    # ------------------------------------------------------------------ 12
    {
        "id": "derivee_monotonie",
        "famille": "Dérivation",
        "titre": "Dérivée et sens de variation",
        "enonce": r"""
Soit $f$ continue sur $[a,b]$ et dérivable sur $]a,b[$.
$$ f'\ge0 \text{ sur } ]a,b[\ \Longrightarrow\ f \text{ est croissante sur } [a,b], $$
$$ f'\le0 \text{ sur } ]a,b[\ \Longrightarrow\ f \text{ est décroissante sur } [a,b]. $$
Si $f'>0$ partout sur $]a,b[$, alors $f$ est strictement croissante.
""",
        "mots": r"""
Le signe de la dérivée est le panneau de signalisation de la pente : $+$ ça monte, $-$ ça descend, $0$ ça fait du plat.

Attention : $f'>0$ est **suffisant** pour être strictement croissant, mais pas nécessaire. La fonction $x^3$ est strictement croissante, et pourtant $f'(0)=0$.
""",
        "preuve": r"""
Prenons $x<y$ dans $[a,b]$. Le théorème des accroissements finis (notion suivante) donne $c\in]x,y[$ tel que
$$ f(y)-f(x)=f'(c)(y-x). $$
Comme $y-x>0$, le signe de $f(y)-f(x)$ est celui de $f'(c)$. Si $f'\ge0$, alors $f(y)\ge f(x)$ : $f$ est croissante.
""",
        "exemple": r"""
$f(x)=x^3-3x$ a pour dérivée $3x^2-3=3(x-1)(x+1)$. Elle est croissante sur $]-\infty,-1]$, décroissante sur $[-1,1]$, croissante sur $[1,+\infty[$.

$f(x)=x+\sin x$ a $f'(x)=1+\cos x\ge0$ : elle est croissante.
""",
        "contre": r"""
$f(x)=x^3$ est strictement croissante sur $\mathbb{R}$ alors que $f'(0)=0$ : on ne peut pas remplacer « $f'\ge0$ » par « $f'>0$ » sans perdre des exemples.

$f'\ge0$ n'implique pas la stricte croissance : une fonction constante a une dérivée nulle.
""",
        "quand": r"""
Pour dresser un tableau de variations, pour prouver une inégalité en étudiant une fonction auxiliaire (exercices 9 et 10), ou pour encadrer $e^x$ et $\ln$.
""",
        "td": "Exercices 9 et 10",
        "graph": g_derivee_monotonie,
    },
    # ------------------------------------------------------------------ 13
    {
        "id": "rolle",
        "famille": "Dérivation",
        "titre": "Théorème de Rolle",
        "enonce": r"""
Soit $f:[a,b]\to\mathbb{R}$ continue sur $[a,b]$, dérivable sur $]a,b[$, avec
$$ f(a)=f(b). $$
Alors il existe $c\in]a,b[$ tel que
$$ f'(c)=0. $$
""",
        "mots": r"""
Tu pars et tu reviens à la même hauteur. Au moins une fois pendant le trajet, tu as roulé à plat : la tangente était horizontale.

C'est le théorème qui prépare le TAF, et qui permet de compter les zéros d'une dérivée.
""",
        "preuve": r"""
$f$ est continue sur le segment $[a,b]$, donc elle y atteint son maximum $M$ et son minimum $m$ (théorème des bornes atteintes).

Si $M=m$, $f$ est constante et $f'=0$ partout : n'importe quel $c$ convient.

Sinon, comme $f(a)=f(b)$, l'une des deux valeurs extrêmes est atteinte en un point $c\in]a,b[$. En un extremum intérieur, la dérivée s'annule : $f'(c)=0$.
""",
        "exemple": r"""
$f(x)=\sin x$ sur $[0,\pi]$ : $f(0)=f(\pi)=0$, et $f'(\pi/2)=\cos(\pi/2)=0$.

$f(x)=x^3-x$ sur $[-1,1]$ : $f(-1)=f(1)=0$, et $f'$ s'annule en $\pm1/\sqrt3$. Rolle ne dit pas que $c$ est unique.
""",
        "contre": r"""
$f(x)=x$ sur $[0,1]$ : $f(0)\neq f(1)$, les hypothèses ne sont pas réunies.

$f(x)=|x|$ sur $[-1,1]$ : $f(-1)=f(1)$, mais $f$ n'est pas dérivable en $0$, et aucune tangente horizontale n'existe. La dérivabilité sur $]a,b[$ est indispensable.
""",
        "quand": r"""
Pour prouver l'existence d'un zéro de $f'$, pour fabriquer le TAF, et pour l'exercice 4.1 et 4.4 (fonction auxiliaire).
""",
        "td": "Exercices 4.1 et 4.4",
        "graph": g_rolle,
    },
    # ------------------------------------------------------------------ 14
    {
        "id": "taf",
        "famille": "Dérivation",
        "titre": "Théorème des accroissements finis (TAF)",
        "enonce": r"""
Soit $f:[a,b]\to\mathbb{R}$ continue sur $[a,b]$, dérivable sur $]a,b[$. Alors il existe $c\in]a,b[$ tel que
$$ f(b)-f(a)=f'(c)(b-a). $$

**Inégalité des accroissements finis.** Si $|f'|\le M$ sur $]a,b[$, alors
$$ |f(b)-f(a)|\le M|b-a|. $$
""",
        "mots": r"""
La pente moyenne entre deux points est toujours réalisée **exactement** par une tangente quelque part entre les deux. La corde et la tangente sont parallèles.

C'est l'outil universel pour majorer une différence $f(b)-f(a)$ par une différence $b-a$.
""",
        "preuve": r"""
On pose
$$ g(x)=f(x)-f(a)-\frac{f(b)-f(a)}{b-a}(x-a). $$
Alors $g(a)=g(b)=0$, $g$ est continue sur $[a,b]$ et dérivable sur $]a,b[$. Rolle donne $c\in]a,b[$ avec $g'(c)=0$, c'est-à-dire
$$ f'(c)-\frac{f(b)-f(a)}{b-a}=0. $$
On isole $f(b)-f(a)$.
""",
        "exemple": r"""
Pour $f=\sin$, $|f'|\le1$, donc $|\sin x-\sin y|\le|x-y|$ pour tous $x,y$.

Pour $f=\ln$ sur $[1,x]$, il existe $c\in]1,x[$ avec $\ln x=\frac{x-1}{c}\le x-1$.
""",
        "contre": r"""
$f(x)=|x|$ sur $[-1,1]$ : $f(1)-f(-1)=0$, mais il n'existe aucun $c$ avec $f'(c)=0$, car $f$ n'est pas dérivable en $0$.

Si $f$ n'est pas continue à une borne, le théorème peut tomber en défaut : la continuité sur le segment entier est nécessaire.
""",
        "quand": r"""
Pour majorer $|f(x)-f(y)|$ (exercice 9.1), pour encadrer $e^x$ et $\ln$ (exercice 9.2 et 9.3), et pour l'inégalité de l'exercice 10.
""",
        "td": "Exercices 9 et 10",
        "graph": g_taf,
    },
    # ------------------------------------------------------------------ 15
    {
        "id": "derivee_nieme",
        "famille": "Dérivation",
        "titre": "Dérivée n-ième",
        "enonce": r"""
On définit par récurrence
$$ f^{(0)}=f,\qquad f^{(n+1)}=\left(f^{(n)}\right)'. $$

Pour tout $n\in\mathbb{N}$ et tout $x\in\mathbb{R}$ :
$$ (\sin x)^{(n)}=\sin\left(x+\frac{n\pi}{2}\right),\qquad (\cos x)^{(n)}=\cos\left(x+\frac{n\pi}{2}\right). $$

$$ (e^{ax})^{(n)}=a^n e^{ax},\qquad (x^p)^{(n)}=\frac{p!}{(p-n)!}\,x^{p-n}\quad(p\in\mathbb{N},\ n\le p). $$
""",
        "mots": r"""
Dériver $n$ fois, c'est appliquer $n$ fois la même machine. Pour $\sin$ et $\cos$, la machine fait tourner le graphe d'un quart de tour à chaque fois : au bout de quatre tours, on retrouve la fonction de départ.

Pour un polynôme, les puissances tombent une à une jusqu'à zéro.
""",
        "preuve": r"""
Pour $\sin$, on dérive $\sin\left(x+\frac{n\pi}{2}\right)$ :
$$ \frac{d}{dx}\sin\left(x+\frac{n\pi}{2}\right)=\cos\left(x+\frac{n\pi}{2}\right)=\sin\left(x+\frac{(n+1)\pi}{2}\right). $$
C'est exactement la formule au rang $n+1$. L'initialisation $n=0$ est immédiate. Le même calcul marche pour $\cos$.
""",
        "exemple": r"""
$(\sin x)^{(4)}=\sin(x+2\pi)=\sin x$. La dérivée quatrième redonne la fonction.

$(\cos x)^{(3)}=\cos\left(x+\frac{3\pi}{2}\right)=\sin x$.
""",
        "contre": r"""
$(fg)^{(n)}\neq f^{(n)}g^{(n)}$. Par exemple $(x^2e^x)''\neq (x^2)''(e^x)''=2e^x$ : il faut la formule de Leibniz.

De même, $(f\circ g)'\neq f'\circ g'$ : la dérivation d'une composée est plus subtile.
""",
        "quand": r"""
Pour l'exercice 8 : calculer la dérivée d'ordre $n$ de $\sin$, $\cos$ et de leurs puissances linéarisées.
""",
        "td": "Exercice 8",
        "graph": g_derivee_nieme,
    },
    # ------------------------------------------------------------------ 16
    {
        "id": "leibniz",
        "famille": "Dérivation",
        "titre": "Formule de Leibniz",
        "enonce": r"""
Si $f$ et $g$ sont $n$ fois dérivables, alors
$$ (fg)^{(n)}=\sum_{k=0}^{n}\binom{n}{k}\,f^{(k)}\,g^{(n-k)}. $$
""",
        "mots": r"""
La dérivée $n$-ième d'un produit ressemble au développement de $(a+b)^n$ : à chaque étape, on choisit de dériver $f$ ou de dériver $g$. Les coefficients binomiaux comptent les choix.

Ce n'est **pas** $f^{(n)}g^{(n)}$ : il y a tous les termes intermédiaires.
""",
        "preuve": r"""
On procède par récurrence sur $n$.

Pour $n=1$, $(fg)'=f'g+fg'$, ce qui est la formule avec $\binom10=\binom11=1$.

Si la formule est vraie au rang $n$, on dérive :
$$ (fg)^{(n+1)}=\sum_{k=0}^{n}\binom{n}{k}\left(f^{(k+1)}g^{(n-k)}+f^{(k)}g^{(n-k+1)}\right). $$
On réindexe et on utilise la relation de Pascal $\binom{n}{k}+\binom{n}{k-1}=\binom{n+1}{k}$.
""",
        "exemple": r"""
Pour $f(x)=x^2$ et $g(x)=e^x$, toutes les dérivées de $f$ d'ordre $\ge3$ sont nulles :
$$ (x^2e^x)^{(n)}=e^x\left(x^2+2nx+n(n-1)\right). $$
""",
        "contre": r"""
$(fg)'=f'g'$ est faux en général : avec $f=g=x$, $(x^2)'=2x$ tandis que $f'g'=1$.

$(fg)''=f''g+2f'g'+fg''$ : il y a bien trois termes, pas deux.
""",
        "quand": r"""
Pour dériver $n$ fois un produit polynôme $\times$ exponentielle, ou pour l'exercice 8 si l'on rencontre un produit.
""",
        "td": "Exercice 8 (variante)",
        "graph": g_leibniz,
    },
    # ------------------------------------------------------------------ 17
    {
        "id": "linearisation",
        "famille": "Dérivation",
        "titre": "Linéarisation trigonométrique",
        "enonce": r"""
Pour tout réel $x$ :
$$ \sin^3x=\frac{3\sin x-\sin 3x}{4},\qquad \cos^3x=\frac{3\cos x+\cos 3x}{4}. $$

Plus généralement, les formules produit-somme transforment un produit de sinus et de cosinus en somme de fonctions trigonométriques simples.
""",
        "mots": r"""
Une puissance de $\sin$ ou $\cos$ est difficile à dériver $n$ fois. Une somme de $\sin(kx)$ et $\cos(kx)$ est facile : chaque dérivation décale la phase.

Linéariser, c'est donc **remplacer une forme compliquée par une somme de vagues simples**, sans changer la fonction.
""",
        "preuve": r"""
On part de la formule d'Euler $\sin x=\frac{e^{ix}-e^{-ix}}{2i}$. En élevant au cube et en développant, les termes $e^{3ix}$ et $e^{-3ix}$ se regroupent en $\sin 3x$, et les termes $e^{ix}$ et $e^{-ix}$ en $\sin x$. On obtient l'identité.

Pour $\cos^3$, on utilise $\cos x=\frac{e^{ix}+e^{-ix}}{2}$.
""",
        "exemple": r"""
$\sin^3x=\frac{3\sin x-\sin 3x}{4}$. En $x=\frac\pi2$ : à gauche $1$, à droite $\frac{3-(-1)}4=1$. L'identité est vérifiée.

$\cos^3x=\frac{3\cos x+\cos 3x}{4}$.
""",
        "contre": r"""
$\sin^2x\neq\sin(x^2)$ : la linéarisation est une **identité exacte**, pas une approximation ni un changement de variable.

$\sin^3x$ n'est pas égal à $\sin(3x)$ : le facteur $\frac14$ et le terme en $\sin x$ sont indispensables.
""",
        "quand": r"""
Pour l'exercice 8 : linéariser $\sin^3x+\cos^3x$ avant de dériver $n$ fois, et plus généralement pour intégrer ou dériver des puissances trigonométriques.
""",
        "td": "Exercice 8",
        "graph": g_linearisation,
    },
    # ------------------------------------------------------------------ 18
    {
        "id": "concavite",
        "famille": "Dérivation",
        "titre": "Concavité",
        "enonce": r"""
$f$ est **concave** sur un intervalle $I$ si, pour tous $x,y\in I$ et tout $t\in[0,1]$,
$$ f\big(tx+(1-t)y\big)\ge t f(x)+(1-t)f(y). $$

$f$ est **convexe** si l'inégalité est dans l'autre sens.

Si $f$ est deux fois dérivable sur $I$ : $f''\le0$ sur $I$ implique $f$ concave ; $f''\ge0$ implique $f$ convexe.
""",
        "mots": r"""
Concave : la courbe est bombée vers le haut, comme une colline. La corde entre deux points passe **sous** la courbe.

Convexe : la courbe est creuse, comme une vallée. La corde passe **au-dessus** de la courbe.
""",
        "preuve": r"""
Si $f''\le0$, alors $f'$ est décroissante. La pente de la corde entre $x$ et $y$ est comprise entre $f'(x)$ et $f'(y)$ (c'est le TAF). En faisant varier le point, on montre que la courbe reste au-dessus de la corde.

Pour une preuve directe, prenons $x<z<y$. Le TAF sur $[x,z]$ donne $c_1\in]x,z[$ avec $f(z)-f(x)=f'(c_1)(z-x)$ ; le TAF sur $[z,y]$ donne $c_2\in]z,y[$ avec $f(y)-f(z)=f'(c_2)(y-z)$. Comme $c_1<c_2$ et que $f'$ est décroissante, $f'(c_1)\ge f'(c_2)$. En réarrangeant, on obtient
$$ f(z)\ge\frac{y-z}{y-x}f(x)+\frac{z-x}{y-x}f(y), $$
c'est-à-dire exactement la concavité.
""",
        "exemple": r"""
$\sin$ est concave sur $[0,\pi]$ : sa dérivée seconde $-\sin$ est $\le0$ sur cet intervalle.

$\ln$ est concave sur $]0,+\infty[$ ; $x^2$ est convexe sur $\mathbb{R}$.
""",
        "contre": r"""
$\sin$ n'est **pas** concave sur $[0,2\pi]$ : sa dérivée seconde change de signe. La concavité se vérifie sur un intervalle, pas sur un domaine discontinu.

$x^3$ n'est ni concave ni convexe sur $\mathbb{R}$ : $f''(x)=6x$ change de signe en $0$.
""",
        "quand": r"""
Pour prouver l'inégalité $(2/\pi)x\le\sin x$ de l'exercice 10, pour les inégalités de convexité, et pour majorer une fonction par sa corde.
""",
        "td": "Exercice 10",
        "graph": g_concavite,
    },
    # ------------------------------------------------------------------ 19
    {
        "id": "bijection",
        "famille": "Bijection et régularité",
        "titre": "Bijection et fonction réciproque",
        "enonce": r"""
$f:E\to F$ est **bijective** si elle est :
- **injective** : $f(x)=f(y)\Longrightarrow x=y$ ;
- **surjective** : pour tout $y\in F$, il existe $x\in E$ tel que $f(x)=y$.

**Théorème de la bijection.** Si $f$ est continue et strictement monotone sur un intervalle $I$, alors $f$ réalise une bijection de $I$ sur $f(I)$, et
$$ f^{-1}:f(I)\to I $$
est continue et strictement monotone, de même sens que $f$.
""",
        "mots": r"""
Bijective : chaque sortie a exactement une entrée. La réciproque défait ce que $f$ fait : $f^{-1}(f(x))=x$ et $f(f^{-1}(y))=y$.

Le théorème dit que la stricte monotonie empêche deux entrées de donner la même sortie, et que le TVI garantit que toutes les sorties intermédiaires sont atteintes.
""",
        "preuve": r"""
**Injectivité.** Si $x\neq y$, disons $x<y$, la stricte monotonie donne $f(x)<f(y)$ (ou $>$), donc $f(x)\neq f(y)$.

**Surjectivité sur $f(I)$.** C'est la définition de $f(I)$. Le TVI montre de plus que $f(I)$ est un intervalle : toutes les valeurs entre $f(x)$ et $f(y)$ sont atteintes.

**Continuité de la réciproque.** Elle découle du théorème de la bijection continue : l'image d'un intervalle par $f$ est un intervalle, et l'application inverse, qui est monotone, ne peut pas avoir de saut.
""",
        "exemple": r"""
$f(x)=\frac{x}{1+|x|}$ réalise une bijection de $\mathbb{R}$ sur $]-1,1[$ ; sa réciproque est $f^{-1}(y)=\frac{y}{1-|y|}$.

$\exp$ réalise une bijection de $\mathbb{R}$ sur $]0,+\infty[$, de réciproque $\ln$.
""",
        "contre": r"""
$x^2$ n'est pas injective sur $\mathbb{R}$ : $(-1)^2=1^2$. Elle devient bijective de $[0,+\infty[$ sur $[0,+\infty[$.

$\sin$ n'est pas injective sur $\mathbb{R}$ : elle l'est seulement sur $[-\pi/2,\pi/2]$.
""",
        "quand": r"""
Pour l'exercice 5, pour résoudre $f(x)=y$ de façon unique, et pour justifier l'existence d'une réciproque avant de la calculer.
""",
        "td": "Exercice 5",
        "graph": g_bijection,
    },
    # ------------------------------------------------------------------ 20
    {
        "id": "c1",
        "famille": "Bijection et régularité",
        "titre": "Dérivée continue : classe C¹",
        "enonce": r"""
$f$ est de **classe $\mathcal{C}^1$** sur un intervalle $I$ si $f$ est dérivable sur $I$ et si $f'$ est continue sur $I$.

Attention : **dérivable n'implique pas $\mathcal{C}^1$**.
""",
        "mots": r"""
Dérivable : il y a une tangente en chaque point. $\mathcal{C}^1$ : en plus, la tangente tourne sans à-coup, sa pente varie continûment.

Une fonction peut avoir une tangente partout et une pente qui oscille de plus en plus vite : c'est le cas de $x^2\sin(1/x)$.
""",
        "preuve": r"""
Pour $f(x)=x^2\sin(1/x)$ prolongée par $f(0)=0$ :
- en $0$, $\frac{f(h)-f(0)}{h}=h\sin(1/h)\to0$, donc $f'(0)=0$ ;
- pour $x\neq0$, la formule usuelle donne $f'(x)=2x\sin(1/x)-\cos(1/x)$.

Or $\cos(1/x)$ n'a pas de limite en $0$ : $f'$ n'est pas continue en $0$. Donc $f$ est dérivable partout, mais pas $\mathcal{C}^1$.
""",
        "exemple": r"""
Les polynômes, $\exp$, $\sin$, $\cos$ sont $\mathcal{C}^1$ sur $\mathbb{R}$.

$x^2\sin(1/x)$ est dérivable sur $\mathbb{R}$ mais sa dérivée n'est pas continue en $0$.
""",
        "contre": r"""
$|x|$ n'est même pas dérivable en $0$ : elle est $\mathcal{C}^0$ mais pas $\mathcal{C}^1$.

Il ne suffit pas que $f'$ existe partout pour qu'elle soit continue : l'exemple $x^2\sin(1/x)$ le prouve.
""",
        "quand": r"""
Pour l'exercice 7, et pour savoir quand on a le droit d'utiliser les théorèmes qui exigent une dérivée continue (composition, inversion locale, etc.).
""",
        "td": "Exercice 7",
        "graph": g_c1,
    },
]

PAR_ID = {notion["id"]: notion for notion in NOTIONS}
NUMERO = {notion["id"]: index + 1 for index, notion in enumerate(NOTIONS)}


# ---------------------------------------------------------------------------
# 2. Barre latérale : recherche, choix, progression
# ---------------------------------------------------------------------------
def _sans_accent(texte: str) -> str:
    """Retire les accents pour permettre une recherche tolérante."""
    decompose = unicodedata.normalize("NFD", texte)
    return "".join(c for c in decompose if unicodedata.category(c) != "Mn").lower()


st.sidebar.markdown("### 🧰 Boîte à outils")
st.sidebar.caption("20 notions · 4 familles")

recherche = st.sidebar.text_input(
    "Rechercher une notion",
    placeholder="Rolle, densité, point fixe...",
)

if recherche.strip():
    mots_clefs = _sans_accent(recherche).split()
    notions_filtrees = [
        notion
        for notion in NOTIONS
        if all(
            mot in _sans_accent(
                f"{notion['titre']} {notion['famille']} {notion['td']} {notion['mots']}"
            )
            for mot in mots_clefs
        )
    ]
else:
    notions_filtrees = list(NOTIONS)

if not notions_filtrees:
    st.sidebar.warning("Aucune notion ne correspond à cette recherche.")
    notions_filtrees = list(NOTIONS)

ids_disponibles = [notion["id"] for notion in notions_filtrees]

# On garde la sélection courante même si elle est filtrée, pour éviter que
# le menu ne saute sans prévenir.
selection_courante = st.session_state.get("tb_notion")
if selection_courante and selection_courante not in ids_disponibles:
    ids_disponibles.insert(0, selection_courante)
if "tb_notion" not in st.session_state or st.session_state["tb_notion"] not in ids_disponibles:
    st.session_state["tb_notion"] = ids_disponibles[0]

notion_id = st.sidebar.selectbox(
    "Choisir une notion",
    ids_disponibles,
    format_func=lambda identifiant: f"{NUMERO[identifiant]:02d} · {PAR_ID[identifiant]['titre']}",
    key="tb_notion",
)

if "tb_vues" not in st.session_state:
    st.session_state["tb_vues"] = []
vues = st.session_state["tb_vues"]
if notion_id not in vues:
    vues.append(notion_id)

if "tb_comprises" not in st.session_state:
    st.session_state["tb_comprises"] = {}
comprises = st.session_state["tb_comprises"]

st.sidebar.markdown("---")
st.sidebar.progress(
    len(set(vues)) / len(NOTIONS),
    text=f"{len(set(vues))} / {len(NOTIONS)} notions explorées",
)
if comprises:
    st.sidebar.caption(
        f"{sum(1 for valeur in comprises.values() if valeur)} notion(s) cochée(s) comme comprise(s)."
    )
st.sidebar.markdown("---")
st.sidebar.caption(
    "Conseil : lis d'abord « en mots simples », manipule le graphe, "
    "puis reviens à l'énoncé formel. Termine par le contre-exemple."
)


# ---------------------------------------------------------------------------
# 3. En-tête
# ---------------------------------------------------------------------------
titre_page(
    "Boîte à outils",
    "Les 20 définitions et théorèmes du TD 3. Pour chacun : l'énoncé, les mots simples, "
    "une image interactive, un exemple, un contre-exemple et le réflexe à avoir.",
    "ANALYSE 1 · CP1 · RÉFÉRENTIEL",
)

st.markdown(
    badge("Limites · 6", "bleu")
    + badge("Continuité · 4", "vert")
    + badge("Dérivation · 8", "orange")
    + badge("Bijection et régularité · 2", "violet"),
    unsafe_allow_html=True,
)

with st.expander("Lexique : les mots techniques utilisés dans cette page", expanded=False):
    st.markdown(
        textwrap.dedent(
            r"""
            | Terme | Sens simple |
            |---|---|
            | **Adhérent** | $x_0$ est adhérent à $D$ si tout intervalle autour de $x_0$ contient un point de $D$. On peut s'approcher de $x_0$ par des points de $D$. |
            | **Voisinage** | Un intervalle ouvert autour d'un point. « Au voisinage de $x_0$ » veut dire « dans un petit intervalle autour de $x_0$ ». |
            | **Segment** | Un intervalle fermé et borné $[a,b]$ avec $a<b$. C'est le cadre du TVI, de Rolle et de Heine. |
            | **Compact** | En dimension 1, un segment. C'est un ensemble fermé et borné : pas de bord infini, pas de trou. |
            | **Bornes atteintes** | Une fonction continue sur un segment $[a,b]$ y atteint son maximum et son minimum. |
            | **Bolzano–Weierstrass** | D'une suite bornée, on peut extraire une sous-suite qui converge. |
            | **Sup / inf** | Le plus petit majorant / le plus grand minorant. Le sup existe toujours dans $\mathbb{R}\cup\{+\infty\}$. |
            | **Densité** | Un ensemble $A$ est dense dans $\mathbb{R}$ si tout intervalle ouvert contient un point de $A$. |
            | **Lipschitzienne** | $f$ est $M$-lipschitzienne si $|f(x)-f(y)|\le M|x-y|$ pour tous $x,y$. |
            | **Classe $\mathcal{C}^1$** | $f$ est dérivable et $f'$ est continue. |
            | **Injection / surjection** | Injective : deux entrées différentes donnent deux sorties différentes. Surjective : toute sortie est atteinte. |
            | **Point fixe** | Un $x$ tel que $f(x)=x$. C'est l'intersection de la courbe avec la diagonale $y=x$. |
            """
        ).strip()
    )

st.info(
    "**Comment travailler cette page ?** Choisis une notion dans le menu de gauche. "
    "Lis l'énoncé formel, puis la version simple, puis manipule le graphique. "
    "Ne coche « j'ai compris » que si tu peux expliquer la notion à voix haute, sans regarder."
)


# ---------------------------------------------------------------------------
# 4. Affichage de la notion choisie
# ---------------------------------------------------------------------------
notion = PAR_ID[notion_id]


def _md(texte: str) -> str:
    """Nettoie l'indentation des textes multilignes (sinon Markdown les voit comme du code)."""
    return textwrap.dedent(texte).strip()


st.markdown(f"## {NUMERO[notion_id]:02d}. {notion['titre']}")
st.markdown(
    badge(notion["famille"], "bleu") + badge("TD : " + notion["td"], "violet"),
    unsafe_allow_html=True,
)

encadre("violet", "L'énoncé formel", texte=_md(notion["enonce"]))
encadre("bleu", "En mots simples", texte=_md(notion["mots"]))

st.markdown("### Voir pourquoi")
notion["graph"]()

col_exemple, col_contre = st.columns(2, gap="large")
with col_exemple:
    encadre("vert", "Un exemple", texte=_md(notion["exemple"]))
with col_contre:
    encadre("orange", "Un contre-exemple", texte=_md(notion["contre"]))

encadre("vert", "Pourquoi c'est vrai (idée de la preuve)", texte=_md(notion["preuve"]))

encadre(
    "violet",
    "Quand l'utiliser ?",
    texte=_md(notion["quand"]) + f"\n\n**Dans le TD :** {notion['td']}.",
)

# Suivi personnel de la notion.
cle_comprise = f"tb_ok_{notion_id}"
if cle_comprise not in st.session_state:
    st.session_state[cle_comprise] = bool(comprises.get(notion_id, False))
comprise = st.checkbox(
    "J'ai compris : je peux expliquer cette notion à voix haute, sans le texte.",
    key=cle_comprise,
)
comprises[notion_id] = comprise

if comprise:
    st.success("Bien. Maintenant, va la réutiliser dans un exercice du TD : c'est là que la mémoire se fixe.")

pied_page()
