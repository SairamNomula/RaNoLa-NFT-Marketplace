import React from 'react'
import './App.css';
import Navbar from './components/pages/Navbar';
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom'
import Home from './components/pages/HomePage/Home'
import Community from './components/pages/Community/Community'
import LiveAucs from './components/pages/LiveAucs/LiveAucs'
import Footer from './components/Footer'

function App() {
  return (
    <Router>
      <Navbar />
      <Switch>
        <Route path='/' exact component={Home}/>
        <Route path='/Community' component={Community}/>
        <Route path='/Live Auctions' component={LiveAucs}/>
      </Switch>
      <Footer />
    </Router>
  );
}

export default App;
