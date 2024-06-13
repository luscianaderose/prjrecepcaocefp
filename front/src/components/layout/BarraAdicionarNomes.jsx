import styles from "./BarraAdicionarNomes.module.css"

function BarraAdicionarNomes(){
    return(
        <div className={`${styles.divAdicionarNomes} cor-fundo2`}>
            <div className="txt-tit3">ADICIONAR NOME NA FILA</div>

            <form className={styles.danForm} action="/adicionar_atendido">
                <input name="nome_atendido" type="text" placeholder="Digite o nome aqui"/>

                <div>
                    <div className={styles.btVidenciaPrece}>
                        <input className={styles.radio} type="radio" id="videncia" name="nome_fila" value="videncia" required/>
                        <label className={styles.label1} for="videncia">
                            <div className={styles.radioTxt}>VIDÊNCIA</div>
                        </label>
                        <input className={styles.radio} type="radio" id="prece" name="nome_fila" value="prece"/>
                        <label className={styles.label2} for="prece">
                            <div className={styles.radioTxt}>PRECE</div>
                        </label>
                    </div>
                </div>

                <div>
                    <input type="checkbox" id="medium" name="medium" value="medium"/>MEDIUM
                </div>

                <div>
                    <button>ADICIONAR</button>
                </div>
            </form>
        </div>
    )
}

export default BarraAdicionarNomes