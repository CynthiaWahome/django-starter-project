const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const path = require("path");
const BundleTracker = require("webpack-bundle-tracker");

const resolve = path.resolve.bind(path, __dirname);

module.exports = (env = {}, argv = {}) => {
  const environment = env.NODE_ENV || process.env.NODE_ENV || 'dev';
  const mode = argv.mode || 'development';
  
  let output;
  let extractCssPlugin;
  let fileLoaderName;
  let publicPath;
  let outputPath;

  switch (environment) {
    case "prod":
      publicPath = "https://example.com/static/bundles/prod/";
      outputPath = resolve("bundles/prod");
      break;
    case "stg":
      publicPath = "https://staging.example.com/static/bundles/stg/";
      outputPath = resolve("bundles/stg");
      break;
    case "dev":
    default:
      publicPath = "http://127.0.0.1:8000/static/bundles/dev/";
      outputPath = resolve("bundles/dev");
      break;
  }

  switch (mode) {
    case "production":
      output = {
        path: outputPath,
        filename: "[chunkhash]/[name].js",
        chunkFilename: "[chunkhash]/[name].[id].js",
        publicPath: publicPath
      };
      extractCssPlugin = new MiniCssExtractPlugin({
        filename: "[chunkhash]/[name].css",
        chunkFilename: "[chunkhash]/[name].[id].css"
      });
      fileLoaderName = "[path][name].[contenthash].[ext]";
      break;

    case "development":
    default:
      output = {
        path: outputPath,
        filename: "[name].js",
        chunkFilename: "[name].js",
        publicPath: publicPath
      };
      extractCssPlugin = new MiniCssExtractPlugin({
        filename: "[name].css",
        chunkFilename: "[name].[id].css"
      });
      fileLoaderName = "[path][name].[ext]";
      break;
  }

  return {
    mode: mode,
    entry: "./index.js",
    output,
    module: {
      rules: [
        {
          test: /\.js$/,
          exclude: /node_modules/,
          use: "babel-loader"
        },
        {
          test: /\.(sa|sc|c)ss$/,
          use: [
            MiniCssExtractPlugin.loader,
            {
              loader: "css-loader",
              options: { sourceMap: true }
            },
            {
              loader: "sass-loader",
              options: {
                sourceMap: true,
                implementation: require("sass")
              }
            }
          ]
        },
        {
          test: /\.(eot|otf|ttf|woff|woff2)(\?v=[0-9.]+)?$/,
          type: "asset/resource",
          generator: {
            filename: "fonts/" + fileLoaderName
          }
        },
        {
          test: /\.(png|svg|jpg)(\?v=[0-9.]+)?$/,
          type: "asset/resource",
          generator: {
            filename: "images/" + fileLoaderName
          }
        }
      ]
    },
    plugins: [
      new BundleTracker({
        path: resolve("bundles"),
        filename: `webpack-bundle.${environment}.json`,
        publicPath: publicPath
      }),
      extractCssPlugin
    ],
    devtool: "source-map"
  };
};
