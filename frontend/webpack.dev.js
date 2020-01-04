const webpack = require("webpack");
const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const WriteFilePlugin = require("write-file-webpack-plugin");

const merge = require("webpack-merge");
const common = require("./webpack.common.js");

require("dotenv").config();

module.exports = merge(common, {
    devtool: "eval-source-map",
    mode: "development",
    entry: [
        "webpack-dev-server/client?http://localhost:3000",
        path.join(__dirname, "js/index.js")
    ],
    output: {
        path: path.join(__dirname, "/dist/"),
        filename: "js/[name].[hash].js",
        publicPath: "/frontend/dist/"
    },
    watch: true,
    plugins: [
        new webpack.HotModuleReplacementPlugin(),
        new webpack.NoEmitOnErrorsPlugin(),
        new HtmlWebpackPlugin({
            inject: false,
            hash: true,
            template:"./html/index.html",
            filename: "html/index.html"
        }),
        new MiniCssExtractPlugin({
            filename: "css/[name].[hash].css",
            chunkFilename: "css/[id].[hash].css"
        }),
        new WriteFilePlugin({
            test: /\.html$/
        })
    ],
    devServer: {
        host: "0.0.0.0",
        port: 3000,
        hotOnly: true,
        publicPath: "/frontend/dist/",
        https: true,
        proxy: {
            "/": {
                target: "https://" + process.env.DOCKER_MACHINE_IP + ":8000",
                secure: false
            }
        }
    },
    resolve: {
        alias: {
            "react-dom": "@hot-loader/react-dom"
        }
    }
});