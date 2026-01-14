import {useEffect, useState} from 'react';
import axios from 'axios';
import _ from 'lodash'
import './App.css'

import loading_gif from '../public/loading.svg';


function App() {
    const [loading, setLoading] = useState(false);
    const [inputText, setInputText] = useState('');
    const [translatedText, setTranslatedText] = useState('')

    const translate = () => {
        setLoading(true);
        axios.post(
            'http://localhost:5111/translate/', {input_text: inputText}
        ).then(function (response) {
            console.log(response.data.translation);
            setTranslatedText(response.data.translation);
            setLoading(false);
        }).catch(function (error) {
            console.log(error);
            setLoading(false);
        })
    }

    useEffect(() => {
        setTranslatedText('');
    }, [inputText]);

  return (
    <>
      <h1>Akatat</h1>

      <p className="read-the-docs">
        Automatic Kartuli Transliteration and Translation
      </p>

        <p><b>Try it:</b></p>
        <p onClick={() => {setInputText("რა გქვიათ")}}>რა გქვიათ? (ra gkviat?)</p>
        <p onClick={() => {setInputText("საიდან ხართ")}}>საიდან ხართ? (saidan khart?)</p>
        <p onClick={() => {setInputText("როგორ იქნება ქართულად")}}>როგორ იქნება ქართულად ...? (rogor ikneba kartulad ...?)</p>
        <p onClick={() => {setInputText("გილოცავ შობა")}}>გილოცავ შობა (gilotsav shoba)</p>


      <div className="card" style={{'minWidth': '800px', 'width': '100%'}}>
          <input
              style={{'width': '80%', 'padding': '12px', 'float': 'left'}}
              value={inputText}
              onChange={e => setInputText(e.target.value)}
          />
          <button
              onClick={() => {translate();}}
              style={{'width': '15%', 'float': 'left'}}
          >Transform</button>

          <br style={{'clear': 'both'}}/>

          {loading &&
            <img src={loading_gif}/>
          }

          {!loading &&
              <>
                  <p>{_.map(translatedText, singleTranslation => { return (
                      singleTranslation['transliterated'] + " "
                  )})}</p>
                  <table>

                  {_.map(translatedText, singleTranslation => { return (
                      <tr>
                          <td style={{'textAlign':'right', 'paddingRight':'10px', 'borderRight':'1px solid gray'}}>{singleTranslation['in']}</td>
                          <td style={{'textAlign':'left', 'paddingLeft':'10px', 'paddingRight':'10px','borderRight':'1px solid gray'}}>{singleTranslation['transliterated']}</td>
                          <td style={{'textAlign':'left', 'paddingLeft':'10px'}}>{singleTranslation['out']}</td>
                          <td style={{'textAlign':'left', 'paddingLeft':'10px', 'color': 'gray'}}><i>{singleTranslation['source_name']}</i></td>
                      </tr>
                      )
                  })}
                  </table>
              </>
            }
      </div>
    </>
  )
}

export default App
