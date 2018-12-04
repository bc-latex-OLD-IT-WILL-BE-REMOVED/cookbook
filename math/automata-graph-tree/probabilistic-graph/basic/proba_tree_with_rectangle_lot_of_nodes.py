# Source: http://tex.stackexchange.com/a/329449/6880

from mistool.latex_use import Build, PPath


template = r"""
\documentclass{article}
\usepackage[utf8x]{inputenc}
\usepackage{ucs}
\usepackage{wasysym}
\usepackage{amssymb}
\usepackage{forest}
\useforestlibrary{linguistics}

\begin{document}
\pagestyle{empty}

\begin{forest}
    for tree = {
        sn edges,
        grow'=0,
        l=2.5cm,
        s sep=0.2cm,
        anchor=west,
        child anchor=west}
    [<<tree>>]
\end{forest}


\subsubsection*{LÉGENDE}

$\blacksquare$ : le mot est dans le dictionnaire français.

\noindent $\blacktriangle$ : le mot commence par "R".

\noindent $\newmoon$ : le mot commence par une voyelle, soit ici par "O" ou "U".

\end{document}
"""


with open("motsfrancais_frgut_unix.txt", mode ="r") as frdico:
    ALL_WORDS = [word.strip() for word in frdico]


def buildtree(letters, previous = []):
    if len(letters) == 1:
        deco = ""
        word = "".join(previous + letters)

        if word.lower() in ALL_WORDS:
            deco = r"$\blacksquare$"

        if word[0] == "R":
            deco = r"$\blacktriangle$"

        elif word[0] in ["O", "U"]:
            deco = r"$\newmoon$"

# CUMUL NON GÉRÉ !!!!
        if deco:
            deco = r"++(4em,0) node{<<0>>}".replace(
                "<<0>>",
                deco
            )

        deco = r"{\draw () ++(3.5em,0) node{$\longrightarrow$ <<0>>} <<1>>;}".replace(
            "<<0>>",
            word
        ).replace(
            "<<1>>",
            deco
        )


        forest = r"[{0}] {1}".format(
            letters[0],
            deco
        )

    else:
        forest = ""

        for char in letters:
            others  = [x for x in letters if x != char]

            subtree = buildtree(
                letters  = others,
                previous = previous + [char]
            )

            forest += "[{0}{1}]".format(char, subtree)

    return forest


latex = template.replace(
    "<<tree>>",
    buildtree(list("ORTU"))
)


latexpath = PPath("proba_tree_with_rectangle_lot_of_nodes.tex")

with latexpath.open(mode ="w") as latexfile:
    latexfile.write(latex)

builder = Build(latexpath)
builder.pdf()
