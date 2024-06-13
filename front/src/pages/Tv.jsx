import styles from "./Tv.module.css"

function Tv(){
    return(
        <>
            {/* <!-- espaco --> */}
            <div className={styles.tvEspaco}></div>

            {/* <!-- divs_videncia_prece --> */}
            <div className={styles.tvVidenciaPrece}>
                {/* <!-- html_camaras_videncia --> */}
                <div className={`${styles.tvVidencia} cor-videncia`}>
                    {/* <!-- html_camaras --> */}
                    <div className={`${styles.tvCamara} cor-fundo2 camara-fechada`}>
                        <div className={styles.tvCamaraFonteNumCamara}>
                            <p className="txt-tv1">2 - VIDÊNCIA</p>
                        </div>
                        <p className="txt-tv2">FECHADA</p>
                    </div>
                    <div className={`${styles.tvCamara} cor-fundo2 camara-fechada`}>
                        <div className={styles.tvCamaraFonteNumCamara}>
                            <p className="txt-tv1">4 - VIDÊNCIA</p>
                        </div>
                        <p className="txt-tv2">FECHADA</p>
                    </div>
                </div>

                {/* <!-- html_camaras_prece --> */}
                <div className={`${styles.tvPrece} cor-prece`}>
                    {/* <!-- html_camaras --> */}
                    <div className={`${styles.tvCamara} cor-fundo2 camara-fechada`}>
                        <div className={styles.tvCamaraFonteNumCamara}>
                            <p className="txt-tv1">3 - PRECE</p>
                        </div>
                        <p className="txt-tv2">FECHADA</p>
                    </div>
                    <div className={`${styles.tvCamara} cor-fundo2 camara-fechada`}>
                        <div className={styles.tvCamaraFonteNumCamara}>
                            <p className="txt-tv1">3A - PRECE</p>
                        </div>
                        <p className="txt-tv2">FECHADA</p>
                    </div>
                </div>
            </div>

            {/* <!-- avisos --> */}
            <div className={`${styles.tvAvisos} cor-fundo2`}> SILÊNCIO &nbsp&nbspCOMPROVANTE EM MÃOS &nbsp&nbspDESLIGUEM OS CELULARES &nbsp&nbspLEIA UM LIVRO DO BALCÃO</div>

            {/* <!-- barra_mensagem --> */}
            <div className={`${styles.tvMensagem} cor-fundo2`}>
                <p className="txt-3">
                    {/* <!-- {lista_mensagens[mensagem]} --> */}
                    Frase frase frase frase frase frase frase frase frase frase.
                </p>
            </div>

            {/* <!-- espaco --> */}
            <div className={styles.tvEspaco}></div>

            {/* <!-- bt_painel --> */}
            <a href="/">
                <button>ACESSAR PAINEL DE CONTROLE</button>
            </a>

        </>
    )
}

export default Tv