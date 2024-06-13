import BarraCabecalho from '../components/layout/BarraCabecalho'
import BarraAdicionarNomes from '../components/layout/BarraAdicionarNomes'
import Camaras from '../components/camaras/Camaras'
import BarraLegenda from '../components/layout/BarraLegenda'
import Menu from '../components/layout/Menu'
import Info from '../components/layout/Info'



function Recepcao(){
    return(
    <>
        <BarraCabecalho/>
        <BarraAdicionarNomes/>
        <Camaras/>
        <BarraLegenda/>
        <Menu/>
        <Info/>
    </>
    )
}

export default Recepcao