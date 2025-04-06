// Endpoint pour liker/déliker
app.post('/content/:id/like', async (req, res) => {
    const { userId } = req.body;
    const contentId = req.params.id;
    
    try {
        // Vérifier si l'utilisateur a déjà liké
        const hasLiked = await pool.query(
            'SELECT EXISTS(SELECT 1 FROM likes WHERE user_id = $1 AND content_id = $2)',
            [userId, contentId]
        );
        
        if (hasLiked.rows[0].exists) {
            // Supprimer le like
            await pool.query(
                'DELETE FROM likes WHERE user_id = $1 AND content_id = $2',
                [userId, contentId]
            );
            res.json({ liked: false });
        } else {
            // Ajouter le like
            await pool.query(
                'INSERT INTO likes (user_id, content_id) VALUES ($1, $2)',
                [userId, contentId]
            );
            res.json({ liked: true });
        }
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Endpoint pour obtenir le nombre de likes
app.get('/content/:id/likes', async (req, res) => {
    const contentId = req.params.id;
    
    try {
        const result = await pool.query(
            'SELECT COUNT(*) FROM likes WHERE content_id = $1',
            [contentId]
        );
        res.json({ count: parseInt(result.rows[0].count) });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});
