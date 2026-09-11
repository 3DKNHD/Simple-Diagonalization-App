"""Informe Streamlit a partir de CalculationResult."""

from __future__ import annotations

import streamlit as st

from .formatters import expr_latex, expr_str, format_walks, matrix_latex
from .graphs import to_dot, to_svg
from .models import CalculationResult


def _latex_matrix(title: str, matrix, numeric: bool = False) -> None:
    st.markdown(title)
    shown = matrix.evalf(6) if numeric else matrix
    st.latex(matrix_latex(shown))


def render_result(result: CalculationResult, numeric: bool = False) -> None:
    status_label = {
        "diagonalizable": "Diagonalizable",
        "jordan": "No diagonalizable (forma de Jordan)",
        "complex_over_R": "No diagonalizable sobre ℝ (autovalores complejos)",
    }[result.status]
    st.info(f"**Estado:** {status_label}")

    for msg in result.messages:
        st.warning(msg)

    st.subheader("Matriz A")
    _latex_matrix("A", result.matrix, numeric)
    if result.det is not None:
        st.latex(rf"\det(A)={expr_latex(result.det)}")

    st.subheader("Paso 1 — Polinomio característico")
    st.latex(rf"p(\lambda)=\det(\lambda I-A)={expr_latex(result.charpoly)}")
    st.caption(
        "Convención habitual: p(λ) = det(λI − A). Los autovectores cumplen (A − λI)x = 0."
    )

    st.subheader("Paso 2 — Autovalores y multiplicidades")
    for info in result.eigenvalues:
        st.markdown(
            f"- **λ = ${expr_latex(info.value)}$** · alg = {info.algebraic} · "
            f"geo = {info.geometric}"
        )
        for i, vec in enumerate(info.basis, start=1):
            st.latex(rf"v_{{{i}}}={matrix_latex(vec)}")
        if info.system_latex and result.matrix.rows <= 4:
            st.markdown("Sistema $(A-\\lambda I)x=0$:")
            st.latex(info.system_latex)

    if result.status == "diagonalizable" and result.P is not None:
        st.subheader("Paso 3 — Matrices P, D y P⁻¹")
        if result.uses_p_transpose:
            st.success("A es simétrica (o P salió ortogonal): **P⁻¹ = Pᵀ**.")
        _latex_matrix("P (autovectores por columnas)", result.P, numeric)
        _latex_matrix("D", result.D, numeric)
        _latex_matrix("P⁻¹", result.P_inv, numeric)
        st.subheader(f"Paso 4 — D^{{{result.power}}}")
        _latex_matrix(rf"D^{{{result.power}}}", result.D_power, numeric)
        st.subheader(f"Paso 5 — A^{{{result.power}}} = P D^{{{result.power}}} P^{{-1}}")
        _latex_matrix(rf"A^{{{result.power}}}", result.result_power, numeric)

    if result.jordan_J is not None:
        st.subheader("Forma de Jordan")
        st.latex(r"A = P J P^{-1}")
        _latex_matrix("P", result.jordan_P, numeric)
        _latex_matrix("J", result.jordan_J, numeric)
        if result.jordan_J_power is not None:
            _latex_matrix(rf"J^{{{result.power}}}", result.jordan_J_power, numeric)
        if result.status != "diagonalizable":
            st.subheader(f"A^{{{result.power}}}")
            _latex_matrix(rf"A^{{{result.power}}}", result.result_power, numeric)

    if result.mode == "graph" and result.result_power is not None:
        st.subheader("Grafo")
        kind = "dirigido" if result.is_directed else "no dirigido"
        st.caption(
            f"El grafo es **{kind}**."
            + (" A ≠ Aᵀ." if result.is_directed else " A = Aᵀ.")
        )
        try:
            st.graphviz_chart(to_dot(result.matrix, directed=result.is_directed))
        except Exception:
            st.markdown(
                to_svg(result.matrix, directed=result.is_directed),
                unsafe_allow_html=True,
            )
        st.subheader("Recorridos (no caminos simples)")
        st.caption(
            f"(Aⁿ)ᵢⱼ cuenta los **recorridos** de longitud {result.power} "
            "del vértice i al j; pueden repetir vértices."
        )
        st.code(format_walks(result), language="text")
        rows = [
            {
                "origen": w.src,
                "destino": w.dst,
                "recorridos": expr_str(w.count),
            }
            for w in result.walks
        ]
        st.dataframe(rows, hide_index=True)

    if result.mode == "algebra" and result.exp_tA is not None:
        st.subheader("exponencial e^{tA}")
        shown = result.exp_tA.evalf(6) if numeric else result.exp_tA
        st.latex(matrix_latex(shown))
