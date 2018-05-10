const path = require('path');
const webpack = require('webpack');
const UglifyJSPlugin = require('uglifyjs-webpack-plugin'); // eslint-disable-line
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin; // eslint-disable-line

module.exports = {
    entry: {
        app: './src/js/main_page.js',
        vendor: [
            'jquery',
            'd3',
            'd3-timelines',
            'knockout',
            'bootstrap'
        ],
    },
    output: {
        filename: 'bundle.js',
        path: path.resolve(__dirname, 'static/dist'),
    },
    devtool: 'eval-cheap-module-source-map',
    module: {
        rules: [{
            test: /\.js$/,
            exclude: /node_modules/,
            loader: 'babel-loader',
            options: {
                presets: ['babel-preset-env'],
            },
        }, {
            test: /\.html$/,
            loader: 'html-loader',
        }, {
            test: /\.css$/,
            loader: 'style-loader!css-loader',
        }, {
            test: /\.scss$/,
            use: [{
                loader: 'style-loader',
            }, {
                loader: 'css-loader',
            },],
        }, {
            test: /\.png$|\?|\.gif($|\?)/,
            loader: 'url-loader?publicPath=/static/dist/&limit=100000',
        }, {
            test: /\.jpg$/,
            loader: 'file-loader',
        }, {
            test: /\.woff($|\?)|\.woff2($|\?)|\.ttf($|\?)|\.eot($|\?)|\.svg($|\?)/,
            loader: 'url-loader',
        }],
    },
    plugins: [
        // new BundleAnalyzerPlugin(),
        new webpack.ProvidePlugin({
            jQuery : 'jquery',
            $: 'jquery',
            jquery: 'jquery',
        }),
        new webpack.LoaderOptionsPlugin({
            minimize: true,
            debug: false,
        }),
        new webpack.optimize.ModuleConcatenationPlugin(),
        new webpack.optimize.CommonsChunkPlugin({
            name: 'vendor',
            filename: 'vendor.bundle.js',
        }),
        new webpack.NamedModulesPlugin(),
    ],
};