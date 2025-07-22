import styles from "./Header.module.css";
import { Link } from "react-router-dom";

export default function Header() {
    return (
        <header className={styles.header}>
            <h1>Device Square</h1>
            <nav>
                <ul>
                    <li>
                        <Link to="/homepage">HOME</Link>
                    </li>
                    <li><a href="#">カテゴリー別</a></li>
                    <li><a href="#">アカウント</a></li>
                    <li><a href="#">ログアウト</a></li>
                </ul>
            </nav>
        </header>
    );
}