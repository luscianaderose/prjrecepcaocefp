import styles from "./Menu.module.css"


function Menu(){
    return(
        <div className={`${styles.divMenuTodo} cor-fundo2`}>
            {/* <!-- tit_menu --> */}
            <p className="txt-tit2">MENU</p>

            {/* <!-- menu1 --> */}
            <div className={`${styles.divMenu} cor-fundo2`}>
                {/* <!-- bt_tv --> */}
                <a href="/tv">
                    <button>TV</button>
                </a>
                {/* <!-- bt_silencio --> */}
                <a href="/silencio">
                    <button>PEDIR SILÊNCIO</button>
                </a>
                {/* <!-- bt_reiniciar --> */}
                <a href="/reiniciar_tudo">
                    <button>REINICAR TUDO</button>
                </a>
            </div>

            {/* <!-- menu2 --> */}
            <div className={`${styles.divMenu} cor-fundo2`}>
                {/* <!-- menu_deschamar --> */}
                <a href="/deschamar/2">
                    <button>DESCHAMAR CAM 2</button>
                </a>
                <a href="/deschamar/4">
                    <button>DESCHAMAR CAM 4</button>
                </a>
                <a href="/deschamar/3">
                    <button>DESCHAMAR CAM 3</button>
                </a>
                <a href="/deschamar/3a">
                    <button>DESCHAMAR CAM 3A</button>
                </a>

            </div>

            {/* <!-- menu3 --> */}
            <div className={`${styles.divMenu} cor-fundo2`}>
                {/* <!-- menu_aumentar_capacidade --> */}
                <a href="/aumentar_capacidade/2">
                    <button>AUMENTAR CAM 2</button>
                </a>
                <a href="/aumentar_capacidade/4">
                    <button>AUMENTAR CAM 4</button>
                </a>
                <a href="/aumentar_capacidade/3">
                    <button>AUMENTAR CAM 3</button>
                </a>
                <a href="/aumentar_capacidade/3a">
                    <button>AUMENTAR CAM 3A</button>
                </a>
            </div>

            {/* <!-- menu4 --> */}
            <div className={`${styles.divMenu} cor-fundo2`}>
                {/* <!-- menu_diminuir_capacidade --> */}
                <a href="/diminuir_capacidade/2">
                    <button>DIMINUIR CAM 2</button>
                </a>
                <a href="/diminuir_capacidade/4">
                    <button>DIMINUIR CAM 4</button>
                </a>
                <a href="/diminuir_capacidade/3">
                    <button>DIMINUIR CAM 3</button>
                </a>
                <a href="/diminuir_capacidade/3a">
                    <button>DIMINUIR CAM 3A</button>
                </a>
            </div>
        </div>

    )
}

export default Menu