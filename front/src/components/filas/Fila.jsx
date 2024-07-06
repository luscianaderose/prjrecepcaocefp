import axios from "axios"
import { useState, useEffect } from 'react'
import styles from "./Fila.module.css"
import editarPng from "../../assets/img/editar.png"
import lixoPng from "../../assets/img/lixo.png"
import setaCimaPng from "../../assets/img/seta-cima.png"
import setaBaixoPng from "../../assets/img/seta-baixo.png"
import observacaoPng from "../../assets/img/observacao.png"
import FormAtendido from "../forms/FormAtendido"
import FilaDupla from "./FilaDupla"
import FormObservacao from "../forms/FormObservacao"

function Fila(props){
    const [abertoEditar, setAbertoEditar] = useState({})
    const [abertoObservacao, setAbertoObservacao] = useState({})
    const editarAtendido = (nomePessoa) => {
        if (abertoEditar[nomePessoa] === true) {
            setAbertoEditar(valoresAnteriores => ({
                ...valoresAnteriores,
                [nomePessoa]:false
            }))
        } else {
            setAbertoEditar(valoresAnteriores => ({
                ...valoresAnteriores,
                [nomePessoa]:true
            }))   
        }
    }

    const adicionarObservacao = (nomePessoa) => {
        if (abertoObservacao[nomePessoa] === true) {
            setAbertoObservacao(valoresAnteriores => ({
                ...valoresAnteriores,
                [nomePessoa]:false
            }))
        } else {
            setAbertoObservacao(valoresAnteriores => ({
                ...valoresAnteriores,
                [nomePessoa]:true
            }))   
        }
    }


    const reposicionar = async (nomeFila, numeroAtendido, moverPara) => {
        const resposta = await axios.get(`http://127.0.0.1:5001/reposicionar_atendido?nome_fila=${nomeFila}&numero_atendido=${numeroAtendido}&mover_para=${moverPara}`)
        window.location.reload()
    }

    useEffect(() => {
        Object.values(props.fila["fila"]).map((pessoa, indice) => {
            setAbertoEditar(valoresAnteriores => ({
                ...valoresAnteriores,
                [pessoa["nome"]]:false
            }))

            setAbertoObservacao(valoresAnteriores => ({
                ...valoresAnteriores,
                [pessoa["nome"]]:false
            }))
        })
    }, [props.fila])

    // console.log("abertoEditar:", abertoEditar, props.fila["atividade"])

    return(
        <div className={`${styles.dvpLista} cor-${props.atividade}`}>
            <p className="txt-tit2">FILA {props.atividade.toUpperCase()}</p>

            {Object.values(props.fila["fila"]).map((pessoa, indice) => (
                
                <p key={indice}>
                    {pessoa["estado"] === "riscado" && <s>{indice + 1}. {pessoa["nome"].toUpperCase()} - {pessoa["camara"]}</s>} 
                    {pessoa["estado"] === "atendendo" && <b>{indice + 1}. {pessoa["nome"].toUpperCase()} - {pessoa["camara"]}</b>} 
                    {pessoa["estado"] !== "atendendo" && pessoa["estado"] !== "riscado" && `${indice + 1}. ${pessoa["nome"].toUpperCase()}`}

                    {/* {indice + 1}. {pessoa["nome"]} */}
                    <a 
                        className={styles.linkEditar} 
                        onClick={() => editarAtendido(pessoa["nome"])}
                        // href="/editar_atendido?nome_fila={nome_fila}&numero_atendido={pessoa.numero}"
                    >
                        <img alt="Editar" src={editarPng} width="16" height="16"/>
                    </a>
                    
                    <a 
                        className={styles.linkRemover} 
                        href={`/remover_atendido?nome_fila=${props.fila["atividade"]}&numero_atendido=${pessoa["numero"]}`}
                    >
                        <img alt="Remover" src={lixoPng} width="16" height="16"/>
                    </a>
                    <a 
                        className={styles.linkReposicionar} 
                        // href="/reposicionar_atendido?nome_fila={nome_fila}&numero_atendido={pessoa.numero}&mover_para=cima"
                        onClick={() => reposicionar(props.fila["atividade"], pessoa["numero"], "cima")}
                    >
                        <img alt="Reposicionar" src={setaCimaPng} width="16" height="16"/>
                    </a>
                    <a 
                        className={styles.linkReposicionar} 
                        // href="/reposicionar_atendido?nome_fila={nome_fila}&numero_atendido={pessoa.numero}&mover_para=baixo"
                        onClick={() => reposicionar(props.fila["atividade"], pessoa["numero"], "baixo")}
                    >
                        <img alt="Reposicionar" src={setaBaixoPng} width="16" height="16"/>
                    </a>

                    {/* <a 
                        className={styles.linkDupla} 
                        href="/dupla?numero_atendido={pessoa.numero}&nome_fila={nome_fila}">
                        <img alt="dupla" src={duplaPng} width="16" height="16"/>
                    </a> */}
                    <FilaDupla 
                        dupla={pessoa["dupla"]}
                        numeroAtendido={pessoa["numero"]}
                        fila={props.fila}
                        nomeFila={props.fila["atividade"]}
                    />

                    <a 
                        className={styles.linkObservacao} 
                        // href="/observacao?nome_fila={nome_fila}&numero_atendido={pessoa.numero}"
                        onClick={() => adicionarObservacao(pessoa["nome"])}
                    >
                        <img alt="Observação" src={observacaoPng} width="16" height="16"/>
                    </a>
                    {pessoa["observacao"]}
                    {/* <a className={styles.linkDupla} href="/cancelar_dupla?numero_atendido={pessoa.numero}&nome_fila={nome_fila}">
                        <img alt="dupla" src={duplaCancelarPng} width="16" height="16"/>
                    </a>
                    <a className={styles.linkDupla}>
                        <img alt="dupla de cima" src={duplaCimaPng} width="16" height="16"/>
                    </a>
                    <a className={styles.linkDupla}>
                        <img alt="dupla de baixo" src={duplaBaixoPng} width="16" height="16"/>
                    </a> */}

                    {abertoEditar[pessoa["nome"]] && <FormAtendido 
                        pessoaEstado={pessoa["estado"]} 
                        pessoaNome={pessoa["nome"]}
                        nomeFila={props.fila["atividade"]}
                        numeroAtendido={pessoa["numero"]}
                    />}
                    {abertoObservacao[pessoa["nome"]] && <FormObservacao
                        observacao={pessoa["observacao"]}
                        numeroAtendido={pessoa["numero"]}
                        nomeFila={props.fila["atividade"]}
                    />}
                </p>
            ))}
        </div>
)
}

export default Fila