import styles from "./Botao.module.css"


function Botao (props){
    return(
        <a className={styles.botao} href={props.href}>
            <button>{props.nomeDoBotao.toUpperCase()}</button>
        </a>
    )
}

export default Botao