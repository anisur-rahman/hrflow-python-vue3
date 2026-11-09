# Deployment notes

This app is set up for local development only. To run it elsewhere:

- Set `POSTGRES_PASSWORD` and `DATABASE_URL` as environment variables (not in `.env`)
- The API binds to `127.0.0.1` by default — update port bindings in `docker-compose.yml` as needed
- Build the frontend for production with `npm run build` and serve the `dist` folder via a static host or nginx
- Add authentication before exposing the API publicly — there is none at the moment
