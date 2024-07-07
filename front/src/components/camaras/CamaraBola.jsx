import styles from "./CamaraBola.module.css"


function CamaraBola(props){
    console.log(props.className)
    return(
        <div className={`${styles.dvpCamaraNumeroGrande} ${props.className}`}>
            {props.numeroCamara}
        </div>
    )
}

export default CamaraBola