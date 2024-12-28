import { useEffect, useState } from 'react';

import spacinov from './spacinov.svg';
import Accordion from '@mui/material/Accordion';
import AccordionDetails from '@mui/material/AccordionDetails';
import AccordionSummary from '@mui/material/AccordionSummary';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';



import './App.css';


function App() {
  const [phoneRanges, setPhoneRanges] = useState([]);
  const [customers, setCustomers] = useState([]);

  function fetchData(url, setter) {
    fetch(url, {
      method: 'GET',
      mode: 'cors',
    })
      .then(response => response.json())
      .then(data => {
        setter(data)
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  }

  useEffect(() => {
    fetchData('/api/phone_ranges', setPhoneRanges);
    fetchData('/api/customers', setCustomers);
  }, [])

  const phoneItems = phoneRanges.map((phoneRange) =>
    <Accordion>
      <AccordionSummary
        expandIcon={<ExpandMoreIcon />}
        id={`summary-${phoneRange.id}`}
      >
        <Typography component="span">{`Phone range: from ${phoneRange.lower} to ${phoneRange.upper}`}</Typography>
      </AccordionSummary>
      <AccordionDetails>
        {phoneRange.phone_numbers.map((phone) =>
          <p>{phone.phone}: {
            customers.filter(customer => customer.id === phone.customer_id).map(customer => customer.name)[0]
          }, allocated on {new Date(phone.allocation_date).toDateString()}</p>
        )}
      </AccordionDetails>
    </Accordion>
  );

  return (

    <div className="App">
      <header className="App-header">
        <img src={spacinov} alt="spacinov"></img>
      </header>
      <div className="main-div">
        {phoneItems}
      </div>
    </div>
  );
}

export default App;
