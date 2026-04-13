import { Card } from "react-bootstrap/";
import { Link } from "react-router-dom";
import { useEffect, useState } from "react";

type Post = {
    post_id: number;
    title: string;
    body: string;
    motive: string;
    merit: string;
    demerit: string;
    rating: number;
    image: string;
    user_id: number;
    created_at: string;
    updated_at: string;
};

export default function HomePage() {
    const [posts, setPosts] = useState<Post[]>([]);
    
    useEffect(() => {
        fetch("http://127.0.0.1:5000/api/get_posts")
            .then((res) => res.json())
            .then((data) => setPosts(data));
    }, []);

    return (
        <>
            <h1>デバイス一覧</h1>
            <Link to="/create" className="btn btn-primary">新規作成</Link>
            <div className="row row-cols-1 row-cols-md-3">
                {posts.map((post) => (
                    <div className="col" key={post.post_id}>
                        <Card style={{width: "18rem"}}>
                            <Card.Body>
                                <Card.Title>{post.title}</Card.Title>
                                <Card.Text>
                                    {post.body}
                                </Card.Text>
                            </Card.Body>
                        </Card>
                    </div>
                ))}
            </div>
        </>
    );
};