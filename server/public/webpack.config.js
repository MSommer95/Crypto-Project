const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');

module.exports = {
    mode: 'development',
    watch: true,
    entry: {
        main: './src/js/index.js',
        sign: './src/js/sign.js'

    },
    plugins: [
        new HtmlWebpackPlugin({
            template: './src/html/index.html',
            filename: 'index.html',
            chunks: ['main'],
        }),
        new HtmlWebpackPlugin({
            template: './src/html/sign.html',
            filename: 'sign.html',
            chunks: ['sign'],
        }),
        new CopyWebpackPlugin([]),
    ],
    devtool: 'inline-source-map',
    output: {
        filename: 'js/[name].js',
        path: path.resolve(__dirname, 'dist'),
        publicPath: "/static/"
    },
    module: {
        rules: [
            {
                test: /\.css$/,
                use: [
                    'style-loader',
                    'css-loader',
                ],
            },
            {
                test: /\.scss$/,
                use: [
                    // MiniCssExtractPlugin.loader,
                    'style-loader',
                    {
                        loader: 'css-loader',
                        options: {
                            sourceMap: true,
                        },
                    },
                    {
                        loader: 'sass-loader',
                        options: {
                            sourceMap: true,
                        },
                    },
                ],
            },
            {
                test: /\.(png|svg|jpg|gif)$/,
                use: {
                    loader: 'file-loader',
                    options: {
                        name: '[name].[hash].[ext]',
                        outputPath: 'img/',
                    },
                },
            },
            {
                test: /\.(woff|woff2|eot|ttf|otf)$/,
                use: {
                    loader: 'file-loader',
                    options: {
                        name: '[name].[hash].[ext]',
                        outputPath: 'fonts/',
                    },
                },
            },
            {
                test: /\.html$/,
                use: ['html-loader']
            }
        ],
    },
};