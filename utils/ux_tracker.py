"""
Celebração de progresso com recompensas visuais.
Motiva o usuário leigo a continuar preenchendo.
"""

import streamlit as st


def celebrate_progress(data: dict):
    """Mostra barra de progresso e celebrações em marcos."""
    total = 0
    filled = 0

    # BMC (9 campos)
    bmc = data.get("bmc", {})
    total += 9
    filled += sum(1 for v in bmc.values() if v and str(v).strip())

    # SWOT (4 quadrantes)
    swot = data.get("swot", {})
    total += 4
    filled += sum(1 for k in ["forcas", "fraquezas", "oportunidades", "ameacas"] 
                  if swot.get(k) and len(swot[k]) > 0)

    # Empresa (4 campos)
    emp = data.get("empresa", {})
    total += 4
    filled += sum(1 for v in emp.values() if v and str(v).strip())

    # 5W2H (mínimo 1 ação)
    acoes = data.get("acao_5w2h", [])
    total += 1
    if acoes and any(a.get("what", "").strip() for a in acoes):
        filled += 1

    pct = (filled / total) * 100 if total > 0 else 0

    st.progress(pct / 100, text=f"Seu planejamento está {pct:.0f}% completo")

    # Celebrações por marco (apenas uma vez por sessão)
    if 20 <= pct < 25 and not st.session_state.get("celebrated_20"):
        st.balloons()
        st.toast("🎉 Você já começou! O primeiro passo é o mais importante.", icon="🎉")
        st.session_state.celebrated_20 = True

    if 50 <= pct < 55 and not st.session_state.get("celebrated_50"):
        st.balloons()
        st.toast("🚀 Metade do caminho! Você está construindo algo valioso.", icon="🚀")
        st.session_state.celebrated_50 = True

    if 90 <= pct < 95 and not st.session_state.get("celebrated_90"):
        st.balloons()
        st.toast("🏆 Quase lá! Seu relatório estratégico está quase pronto.", icon="🏆")
        st.session_state.celebrated_90 = True
