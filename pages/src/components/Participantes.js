import '../App.css';

const participantes = ["Daniel Nogueira", "Felipe Moreira", "Lucas Bernardes", "Matheus Geraldino"];

function Participantes() {
    return (
        <div className="Participantes">
            <div className="Participantes-Titulo">Participantes</div>
            <div className="Participantes-Lista">
                {participantes.map((nome, index) => (
                    <div key={index} className="Participantes-Item">
                        {nome}
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Participantes;