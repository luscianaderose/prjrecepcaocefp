import styles from "./Fila.module.css"

function Fila(props){
    return(
        <div className={`${styles.dvpLista} cor-${props.atividade}`}>
            <p className="txt-tit2">FILA {props.atividade.toUpperCase()}</p>
        </div>
)
}

export default Fila