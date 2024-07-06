import styles from "./TvPage.module.css"
import Tvs from "../components/tvs/Tvs"

function TvPage(){

    console.log("styles", styles.tvPainel)

    return(
        <>
            {/* <!-- espaco --> */}
            <div className={styles.tvEspaco}></div>

            <Tvs/>

            {/* <!-- espaco --> */}
            <div className={styles.tvEspaco}></div>

            {/* <!-- bt_painel --> */}
            <div className={styles.tvPainel}>
                <a href="/">
                    <button>ACESSAR PAINEL DE CONTROLE</button>
                </a>
            </div>

        </>
    )
}

export default TvPage