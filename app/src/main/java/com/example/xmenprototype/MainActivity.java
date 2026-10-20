package com.example.xmenprototype;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.view.View;

public class MainActivity extends Activity {
  @Override public void onCreate(Bundle state) {
    super.onCreate(state);
    getWindow().getDecorView().setSystemUiVisibility(5894 | 1024 | 512 | 4096);
    WebView view = new WebView(this);
    WebSettings settings = view.getSettings();
    settings.setJavaScriptEnabled(true);
    settings.setDomStorageEnabled(true);
    settings.setAllowFileAccess(true);
    view.setWebChromeClient(new WebChromeClient());
    setContentView(view);
    view.loadUrl("file:///android_asset/index.html");
  }
  @Override public void onBackPressed() { super.onBackPressed(); }
}
