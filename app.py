"""App Streamlit: potencias por diagonalización exacta."""

from __future__ import annotations

import streamlit as st

from matrix_diagonalization.engine import analyze, parse_matrix_text
from matrix_diagonalization.examples import EXAMPLES, default_grid
from matrix_diagonalization.exceptions import InvalidMatrixError
from matrix_diagonalization.pdf_report import build_pdf_bytes
from matrix_diagonalization.ui_report import render_result

st.set_page_config(
    page_title="Potencias por diagonalización",
    page_icon="▣",
    layout="wide",
)


def _init_state() -> None:
    defaults = {
        "mode_label": "Álgebra",
        "field_label": "ℝ",
        "size": 3,
        "power": 2,
        "grid": default_grid(3, "algebra"),
        "paste": "",
        "example": "Simétrica ponderada",
        "grid_version": 0,
        "result": None,
        "error": None,
        "numeric": False,
        "mode": "algebra",
        "field": "R",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _apply_example() -> None:
    example = EXAMPLES[st.session_state.example]
    st.session_state.mode_label = "Grafo" if example["mode"] == "graph" else "Álgebra"
    st.session_state.field_label = "ℂ" if example["field"] == "C" else "ℝ"
    st.session_state.mode = example["mode"]
    st.session_state.field = example["field"]
    st.session_state.size = example["size"]
    st.session_state.power = example["power"]
    st.session_state.grid = [[str(v) for v in row] for row in example["matrix"]]
    st.session_state.paste = "\n".join(
        " ".join(str(v) for v in row) for row in example["matrix"]
    )
    st.session_state.grid_version += 1
    st.session_state.result = None
    st.session_state.error = None


def _resize_grid(size: int, mode: str) -> None:
    old = st.session_state.grid
    fresh = default_grid(size, mode)
    for i in range(min(size, len(old))):
        for j in range(min(size, len(old[i]))):
            fresh[i][j] = str(old[i][j])
    st.session_state.grid = fresh


def _grid_from_editor(edited, size: int) -> list:
    rows = []
    for i in range(size):
        row = []
        for j in range(size):
            col = f"c{j + 1}"
            if hasattr(edited, "iloc"):
                row.append(str(edited.iloc[i][col]))
            elif isinstance(edited, dict):
                row.append(str(edited[col][i]))
            else:
                row.append(str(edited[i][j]))
        rows.append(row)
    return rows


def _use_pasted_matrix() -> None:
    try:
        parsed = parse_matrix_text(st.session_state.paste)
    except InvalidMatrixError as exc:
        st.session_state.error = str(exc)
        st.session_state.result = None
        return
    if parsed.rows < 2 or parsed.rows > 10:
        st.session_state.error = "El orden de A debe estar entre 2 y 10."
        st.session_state.result = None
        return
    st.session_state.size = parsed.rows
    st.session_state.grid = [
        [str(parsed[i, j]) for j in range(parsed.cols)] for i in range(parsed.rows)
    ]
    st.session_state.grid_version += 1
    st.session_state.result = None
    st.session_state.error = None


def _reset_grid() -> None:
    st.session_state.grid = default_grid(int(st.session_state.size), st.session_state.mode)
    st.session_state.grid_version += 1
    st.session_state.result = None
    st.session_state.error = None


def _sync_mode_and_size() -> None:
    mode = "graph" if st.session_state.mode_label == "Grafo" else "algebra"
    field = "C" if st.session_state.field_label == "ℂ" else "R"
    size = int(st.session_state.size)
    changed = False
    if mode != st.session_state.mode:
        st.session_state.mode = mode
        _resize_grid(size, mode)
        changed = True
    elif len(st.session_state.grid) != size:
        _resize_grid(size, mode)
        changed = True
    st.session_state.field = field
    if changed:
        st.session_state.grid_version += 1
        st.session_state.result = None
        st.session_state.error = None


def main() -> None:
    _init_state()

    st.title("Potencias por diagonalización")
    st.caption("Aⁿ = P Dⁿ P⁻¹ cuando A es diagonalizable. Cálculo exacto con sympy.")

    with st.sidebar:
        st.header("Configuración")
        st.radio("Modo", ("Álgebra", "Grafo"), key="mode_label")
        st.radio("Cuerpo", ("ℝ", "ℂ"), key="field_label")
        st.number_input(
            "Orden de A (n×n)", min_value=2, max_value=10, step=1, key="size"
        )
        st.number_input(
            "Potencia n (negativa si A es invertible)",
            min_value=-20,
            max_value=50,
            step=1,
            key="power",
        )
        st.checkbox("Aproximación numérica (evalf)", key="numeric")
        _sync_mode_and_size()

        st.subheader("Ejemplos")
        st.selectbox("Cargar ejemplo", list(EXAMPLES.keys()), key="example")
        st.button("Cargar ejemplo", width="stretch", on_click=_apply_example)
        st.caption(EXAMPLES[st.session_state.example]["note"])

    tab_grid, tab_paste = st.tabs(["Grilla", "Pegar texto"])
    size = int(st.session_state.size)

    with tab_grid:
        data = {
            f"c{j + 1}": [st.session_state.grid[i][j] for i in range(size)]
            for j in range(size)
        }
        edited = st.data_editor(
            data,
            num_rows="fixed",
            width="stretch",
            key=f"grid_editor_{st.session_state.grid_version}_{size}",
            column_config={
                f"c{j + 1}": st.column_config.TextColumn(f"c{j + 1}")
                for j in range(size)
            },
        )
        st.session_state.grid = _grid_from_editor(edited, size)

    with tab_paste:
        st.text_area(
            "Matriz (espacios o comas; fracciones como 1/2)",
            height=140,
            key="paste",
        )
        st.button("Usar texto pegado", on_click=_use_pasted_matrix)

    col_run, col_clear = st.columns(2)
    run = col_run.button("Calcular Aⁿ", type="primary", width="stretch")
    col_clear.button("Reiniciar grilla", width="stretch", on_click=_reset_grid)

    if run:
        try:
            st.session_state.result = analyze(
                st.session_state.grid,
                power=int(st.session_state.power),
                field=st.session_state.field,
                mode=st.session_state.mode,
                compute_exp=st.session_state.mode == "algebra",
            )
            st.session_state.error = None
        except InvalidMatrixError as exc:
            st.session_state.result = None
            st.session_state.error = str(exc)
        except Exception as exc:
            st.session_state.result = None
            st.session_state.error = f"Error inesperado: {exc}"

    if st.session_state.error:
        st.error(st.session_state.error)

    result = st.session_state.result
    if result is not None:
        render_result(result, numeric=bool(st.session_state.numeric))
        st.download_button(
            "Descargar PDF",
            data=build_pdf_bytes(result),
            file_name="diagonalizacion.pdf",
            mime="application/pdf",
            key="pdf_download",
        )


if __name__ == "__main__":
    main()
