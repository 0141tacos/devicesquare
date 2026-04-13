import styles from "./Footer.module.css"

export default function Footer() {
    return (
        <footer className={styles.footer}>
            <p>デバイス好きが集まり交流するサイト</p>
            <ul>
                <li>サイト運営者: taco5</li>
                <li>X: <a href="https://x.com/0141tacos">@0141tacos</a></li>
            </ul>
        </footer>
    )
}
