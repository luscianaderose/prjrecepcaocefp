import styles from "./CamaraBolinhas.module.css"
import axios from "axios"

function CamaraBolinhas(props){

    const qtdBolinhasTotais = props.capacidade
    const qtdBolinhasPretas = props.numeroAtendimentos
    const qtdBolinhasBrancas = qtdBolinhasTotais - qtdBolinhasPretas
    const bolinhaBranca = String.fromCharCode(9898)
    const bolinhaPreta = String.fromCharCode(9899)


    // console.log("ver aqui", qtdBolinhasTotais, qtdBolinhasPretas, qtdBolinhasBrancas)

    const adicionarBolinhas = async () => {
        const resposta = await axios.get(`http://127.0.0.1:5001/bolinhas?modo=adicao&numero_camara=${props.numero}`)
        window.location.reload()
    }

    const subtrairBolinhas = async () => {
        const resposta = await axios.get(`http://127.0.0.1:5001/bolinhas?modo=subtracao&numero_camara=${props.numero}`)
        window.location.reload()
    }

    return (
        <>
            <a 
                className={`${styles.linkBolinhas} a`} 
                onClick={subtrairBolinhas}
                // href={`/bolinhas?modo=subtracao&numero_camara=${props.numero}`}
            >
                <b>-</b>
            </a>
            {/* <!-- {camara.bolinhas()} --> */}
            {bolinhaPreta.repeat(qtdBolinhasPretas)}
            {bolinhaBranca.repeat(qtdBolinhasBrancas)}
            <a 
                className={`${styles.linkBolinhas} a`} 
                onClick={adicionarBolinhas}
                // href={`/bolinhas?modo=adicao&numero_camara=${props.numero}`}
            >
                <b>+</b>
            </a>
        </>
    )
}

export default CamaraBolinhas