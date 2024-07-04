import axios from "axios"
import { useEffect, useState } from "react"
import styles from "./BarraAdicionarNomes.module.css"

function BarraAdicionarNomes(){
    const [nomeAtendido, setNomeAtendido] = useState()
    const [nomeFila, setNomeFila] = useState()
    const [filaVidencia, setFilaVidencia] = useState()
    const [filaPrece, setFilaPrece] = useState()

    useEffect(() => {
        const buscarFilas = async () => {
            const respostaVidencia = await axios.get("http://127.0.0.1:5001/fila_videncia")
            const respostaPrece = await axios.get("http://127.0.0.1:5001/fila_prece")
            setFilaVidencia(respostaVidencia.data)
            setFilaPrece(respostaPrece.data)
        }
        buscarFilas()
    },[])
    // console.log("fila videncia:", filaVidencia)
    // console.log("fila prece:", filaPrece)
    const adicionarNomeNaFila = async (evento) => {
        evento.preventDefault()
        if (
            nomeFila === "videncia" && 
            Object.values(filaVidencia.fila).map((pessoa,indice) => (
                pessoa["nome"].toUpperCase())
            ).includes(nomeAtendido.toUpperCase())
        ){
            alert("É preciso digitar um nome diferente!")
        }else if (
            nomeFila === "prece" &&
            Object.values(filaPrece.fila).map((pessoa,indice) => (
                pessoa["nome"].toUpperCase())
            ).includes(nomeAtendido.toUpperCase())
        ){
            alert("É preciso digitar um nome diferente!")
        }else if (nomeAtendido === undefined) {
            alert("É preciso digitar um nome!")
        }else if (nomeFila === undefined) {
            alert("É preciso escolher  fila!")
        }else {
            const resposta = await axios.get(`http://127.0.0.1:5001/adicionar_atendido?nome_fila=${nomeFila}&nome_atendido=${nomeAtendido}`)
            window.location.reload()
        }
    }

    return(
        <div className={`${styles.divAdicionarNomes} cor-fundo2`}>
            <div className="txt-tit3">ADICIONAR NOME NA FILA</div>

            <form className={styles.danForm} onSubmit={adicionarNomeNaFila}>
                <input 
                    name="nome_atendido" 
                    type="text" 
                    placeholder="Digite o nome aqui"
                    value={nomeAtendido}
                    onChange={(evento) => setNomeAtendido(evento.target.value)}
                />

                <div>
                    <div className={styles.btVidenciaPrece}>
                        <input 
                            className={styles.radio} 
                            type="radio" 
                            id="videncia" 
                            name="nome_fila" 
                            value="videncia"
                            onChange={(evento) => setNomeFila(evento.target.value)} 
                        />
                        <label className={styles.label1} for="videncia">
                            <div className={styles.radioTxt}>VIDÊNCIA</div>
                        </label>
                        <input 
                            className={styles.radio} 
                            type="radio" 
                            id="prece" 
                            name="nome_fila" 
                            value="prece"
                            onChange={(evento) => setNomeFila(evento.target.value)}
                        />
                        <label className={styles.label2} for="prece">
                            <div className={styles.radioTxt}>PRECE</div>
                        </label>
                    </div>
                </div>

                {/* BOTAO DO MÉDIUM PRA FAZER DEPOIS */}
                {/* <div>
                    <input type="checkbox" id="medium" name="medium" value="medium"/>MEDIUM
                </div> */}

                <div>
                    <button>ADICIONAR</button>
                </div>
            </form>
        </div>
    )
}

export default BarraAdicionarNomes