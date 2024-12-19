import logo from './images/logo.jpeg'
import './App.css';
import githublogo from './images/github-mark-white.png'
import apresentacao from './images/apresentacao.png'
import Header from './components/Header';
import Participantes from './components/Participantes';
import Footer from './components/Footer';

function App() {
  return (
    <div className="App">
      <Header />
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <div className="Links-Container">
          <a
            className="Link-Box"
            href="https://github.com/nogueiralegacy/easypark"
            
            rel="noopener noreferrer"
          >
            <img src={githublogo} alt="githublogo" />
            Github
          </a>
          <a
            className="Link-Box"
            href="https://www.canva.com/design/DAGVKa_tIgU/Hu9NsimnYxCRJ8e1I50_og/edit"
            
            rel="noopener noreferrer"
          >
            <img src={apresentacao} alt="apresentacao" />
            Apresentação
          </a>
        </div>
        <Participantes />
      </header>
      <Footer />
    </div>
  );
}
export default App;
