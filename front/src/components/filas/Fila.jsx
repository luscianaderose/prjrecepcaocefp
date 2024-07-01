import { useState, useEffect } from 'react'
import styles from "./Fila.module.css"
import editarPng from "../../assets/img/editar.png"
import lixoPng from "../../assets/img/lixo.png"
import setaCimaPng from "../../assets/img/seta-cima.png"
import setaBaixoPng from "../../assets/img/seta-baixo.png"
import duplaPng from "../../assets/img/dupla.png"
import duplaCancelarPng from "../../assets/img/dupla_cancelar.png"
import duplaCimaPng from "../../assets/img/dupla_cima.png"
import duplaBaixoPng from "../../assets/img/dupla_baixo.png"
import observacaoPng from "../../assets/img/observacao.png"
import FormAtendido from "../forms/FormAtendido"

function Fila(props){
    const [exibir, setExibir] = useState(false)
    const [abertoEditar, setAbertoEditar] = useState({})
    const editarAtendido = () => {
        setExibir(true)
    }
    // {setTeste({...state, fila["nome"]: false})}
    // Object.values(props.fila["fila"]).forEach((fila) => 
    //     console.log("FILA", fila)
    //     setTeste(prevState => ({
    //         ...prevState,
    //         [fila["nome"]]: false
    //     }));
    // );

    // Object.values(props.fila["fila"]).forEach((fila) => console.log("FILA", fila));

    return(
        <div className={`${styles.dvpLista} cor-${props.atividade}`}>
            <p className="txt-tit2">FILA {props.atividade.toUpperCase()}</p>

            {Object.values(props.fila["fila"]).map((pessoa, indice) => (
                
                <p>
                    {pessoa["estado"] === "riscado" && <s>{indice + 1}. {pessoa["nome"]} - {pessoa["camara"]}</s>} 
                    {pessoa["estado"] === "atendendo" && <b>{indice + 1}. {pessoa["nome"]} - {pessoa["camara"]}</b>} 
                    {pessoa["estado"] !== "atendendo" && pessoa["estado"] !== "riscado" && `${indice + 1}. ${pessoa["nome"]}`}

                    {/* {indice + 1}. {pessoa["nome"]} */}
                    <a 
                        className={styles.linkEditar} 
                        onClick={() => editarAtendido()}
                        // href="/editar_atendido?nome_fila={nome_fila}&numero_atendido={pessoa.numero}"
                    >
                        <img alt="Editar" src={editarPng} width="16" height="16"/>
                    </a>
                    
                    <a className={styles.linkRemover} href="/remover_atendido?nome_fila={nome_fila}&numero_atendido={pessoa.numero}">
                        <img alt="Remover" src={lixoPng} width="16" height="16"/>
                    </a>
                    <a className={styles.linkReposicionar} href="/reposicionar_atendido?nome_fila={nome_fila}&numero_atendido={pessoa.numero}&mover_para=cima">
                        <img alt="Reposicionar" src={setaCimaPng} width="16" height="16"/>
                    </a>
                    <a className={styles.linkReposicionar} href="/reposicionar_atendido?nome_fila={nome_fila}&numero_atendido={pessoa.numero}&mover_para=baixo">
                        <img alt="Reposicionar" src={setaBaixoPng} width="16" height="16"/>
                    </a>
                    <a className={styles.linkDupla} href="/dupla?numero_atendido={pessoa.numero}&nome_fila={nome_fila}">
                        <img alt="dupla" src={duplaPng} width="16" height="16"/>
                    </a>
                    <a className={styles.linkObservacao} href="/observacao?nome_fila={nome_fila}&numero_atendido={pessoa.numero}">
                        <img alt="Observação" src={observacaoPng} width="16" height="16"/>
                    </a>
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
                    filaNome={props.fila["atividade"]}
                    numeroAtendido={pessoa["numero"]}

                    />}

                </p>
            ))}
        </div>
)
}

export default Fila