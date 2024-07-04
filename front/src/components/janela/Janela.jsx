import styles from "./Janela.module.css"

function Janela (props){
    return(
        <>
            <p>{props.texto}</p>
            <div className={styles.btsJanela}>
                <a href={props.href1}>
                    <button className={styles.btj} onClick={props.clickBt1}>{props.bt1}</button>
                </a>
                <a href={props.href2}>
                    <button className={styles.btj}>{props.bt2}</button>
                </a>
            </div>
        </>
    )
}

export default Janela