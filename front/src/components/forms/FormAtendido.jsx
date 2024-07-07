import { useState } from "react"
import axios from "axios"

function FormAtendido (props) {
    const [nomeAtendido, setNomeAtendido] = useState(props.pessoaNome)
    const editarAtendido = async (evento) => {
        evento.preventDefault()
        const resposta = await axios.get(`http://127.0.0.1:5001/editar_atendido_confirmado?nome_fila=${props.nomeFila}&numero_atendido=${props.numeroAtendido}&nome_atendido=${nomeAtendido}`)
        window.location.reload()
    }

    const desriscar = async () => {
        const resposta = await axios.get(`http://127.0.0.1:5001/desriscar?numero_atendido=${props.numeroAtendido}&nome_fila=${props.nomeFila}`)
        window.location.reload()
    }

    const linha = (
        <><br></br>____________________________________________________________<br></br><br></br></>
    )

    return (
        <>
            <p>Deseja editar o nome?</p>
            <form onSubmit={(evento) => editarAtendido(evento)}>
                <input 
                    type='text' 
                    name='nome_atendido' 
                    value={nomeAtendido} 
                    onChange={(evento) => setNomeAtendido(evento.target.value)}
                />
                <input type='hidden' name='nome_fila' value={props.nomeFila}/>
                <input type='hidden' name='numero_atendido' value={props.numeroAtendido}/>
                <button type='submit' className='btj'>CONFIRMAR</button>
            </form>
            {
                props.pessoaEstado === "riscado" && (
                    <>
                    {linha}
                    <p>Deseja desriscar o nome?</p>
                    <a onClick={() => desriscar()}>
                        <button>DESRISCAR</button>
                    </a>
                    {linha}
                    Cancelar
                    </>
                )
            }
        </>
    )
}

export default FormAtendido