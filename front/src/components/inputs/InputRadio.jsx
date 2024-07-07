import styles from "./InputRadio.module.css"


function InputRadio(props){
    return(
        <>
            <input 
                className={styles.radio} 
                type="radio" 
                id={props.id}
                name={props.name} 
                value={props.value}
                onChange={props.onChange} 
            />
            <label className={styles.label1} for={props.id}>
                <div className={styles.radioTxt}>{props.label.toUpperCase()}</div>
            </label>
        </>
    )
}

export default InputRadio

{/* <input 
className={styles.radio} 
type="radio" 
id="videncia" 
name="nome_fila" 
value="videncia"
onChange={(evento) => setNomeFila(evento.target.value)} 
/>
<label className={styles.label1} for="videncia">
<div className={styles.radioTxt}>VIDÊNCIA</div>
</label> */}
