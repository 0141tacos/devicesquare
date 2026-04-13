import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ROUTES_PATH } from './pages/const';
import LoginPage from './pages/LoginPage';
import HomePage from './pages/HomePage/HomePage';
import Header from './components/Header/Header';
import Footer from './components/Footer/Footer';
import styles from "./App.module.css";

function App() {
  return (
    <>
      <BrowserRouter>
        <Header />
        <div className={styles.appcontent}>
          <Routes>
            <Route path={ROUTES_PATH.LOGIN} element={<LoginPage />} />
            <Route path={ROUTES_PATH.HOME} element={<HomePage />} />
          </Routes>
        </div>
        <Footer />
      </BrowserRouter>
    </>
  );
};

export default App;
