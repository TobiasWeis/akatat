import {useEffect, useState} from 'react';
import axios from 'axios';
import './App.css'


function App() {
    const [inputText, setInputText] = useState('');
    const [outputText, setOutputText] = useState('');
    const [translatedText, setTranslatedText] = useState('')

    useEffect(() => {
        transliterate();
    }, [inputText]);

    useEffect(() => {
        // TODO: check if there is a space (meaning: we have full words)
        translate();
    }, [outputText])

    const translate = () => {
        axios.post(
            'http://localhost:5000/translate/', {input_text: inputText}
        ).then(function (response) {
            console.log(response.data.translation);
            setTranslatedText(response.data.translation);
        }).catch(function (error) {
            console.log(error);
        })
    }

    const transliterate = () => {
        // send to backend to transliterate
        axios.post('http://localhost:5000/transliterate/', {
            input_text: inputText,
          })
          .then(function (response) {
            console.log(response);
            setOutputText(response.data.transliterated);
          })
          .catch(function (error) {
            console.log(error);
          });
    }

  return (
    <>
      <h1>Akatat</h1>

      <p className="read-the-docs">
        Automatic Kartuli Transliteration and Translation
      </p>

      <div className="card" style={{'minWidth': '80%'}}>
          <input
              style={{'width': '100%', 'padding': '12px'}}
              value={inputText}
              onChange={e => setInputText(e.target.value)}
          />
          <p>{outputText}</p>
          <p>{translatedText}</p>
      </div>
    </>
  )
}

export default App
