const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const ImageminPlugin = require("imagemin-webpack-plugin").default;
const FlowWebpackPlugin = require("flow-webpack-plugin");
 
const devMode = process.argv[3] !== "production";


module.exports = {
    module: {
        rules: [
            {
                test: /\.txt$/,
                use: "raw-loader"
            },
            {
                test: /\.jsx?$/,
                use: {
                    loader: "babel-loader",
                    options: {
                        presets: ['@babel/preset-env']
                    }
                },
                exclude: /node_modules/
            },
            {
                test: /\.css$/,
                use: [devMode ? "style-loader" : MiniCssExtractPlugin.loader, "css-loader"]
            },
            {
                test: /\.(woff|woff2)(\?v=\d+\.\d+\.\d+)?$/,
                use: [
                    {
                        loader: "url-loader",
                        options: {
                            limit: 10000,
                            mimetype: "application/font-woff",
                            name: "./fonts/[hash].[ext]"
                        }
                    }
                ]
            },
            {
                test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/,
                use: [
                    {
                        loader: "url-loader",
                        options: {
                            limit: 10000,
                            mimetype: "application/octet-stream",
                            name: "./fonts/[hash].[ext]"
                        }
                    }
                ]
            },
            {
                test: /\.eot(\?v=\d+\.\d+\.\d+)?$/,
                use: [
                    {
                        loader: "file-loader",
                        options: {
                            limit: 10000,
                            name: "./fonts/[hash].[ext]"
                        }
                    }
                ]
            },
            {
                test: /\.svg(\?v=\d+\.\d+\.\d+)?$/,
                use: [
                    {
                        loader: "url-loader",
                        options: {
                            limit: 10000,
                            mimetype: "image/svg+xml",
                            name: "./fonts/[hash].[ext]"
                        }
                    }
                ]
            },
            {
                test: /\.(jpe?g|png|gif|ico)$/i,
                use: [
                    {
                        loader: "file-loader",
                        options: {
                            hash: "sha512",
                            digest: "hex",
                            name: "./img/[hash].[ext]"
                        }
                    }
                ]
            }
        ]
    },
    plugins: [
        new ImageminPlugin({
            test: /\.(jpe?g|png|gif|svg)$/i
        }),
        new FlowWebpackPlugin()
    ],
    resolve: {
        alias: {
            willbuyer: path.resolve(__dirname),
            css: path.resolve(__dirname, "css"),
            components: path.resolve(__dirname, "js", "components"),
            contexts: path.resolve(__dirname, "js", "contexts"),
            hooks: path.resolve(__dirname, "js", "hooks"),
            img: path.resolve(__dirname, "img"),
            lib: path.resolve(__dirname, "js", "lib")
        }
    }
};
