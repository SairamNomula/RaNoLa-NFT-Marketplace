import React from 'react'
import './App.css';
import Navbar from './components/pages/Navbar';
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom'
import Home from './components/pages/HomePage/Home'
import Community from './components/pages/Community/Community'
import Contact from './components/pages/Contact/Contact'
import Footer from './components/pages/Footer/Footer'

function App() {
  return (
    <Router>
      <Navbar />
      <Switch>
        <Route path='/' exact component={Home}/>
        <Route path='/Community' exact component={Community}/>
        <Route path='/Contact' exact component={Contact}/>
      </Switch>
      <Footer />
    </Router>
  );
}

export default App;
