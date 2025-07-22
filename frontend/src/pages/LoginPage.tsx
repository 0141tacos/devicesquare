import { Card } from "react-bootstrap";

export default function LoginPage() {
    return (
        <Card style={{ width: '18rem' }}>
            <Card.Title>Login</Card.Title>
            <form>
                <label htmlFor="名前">名前</label>
                <input id="name" type="text" />
                <label htmlFor="メールアドレス">メールアドレス</label>
                <input id="email" type="email" />
                <label htmlFor="パスワード">パスワード</label>
                <input id="password" type="password" />

                <button type="submit">送信</button>
            </form>
        </Card>
    );
};