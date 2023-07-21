import Fingerprint2 from "@fingerprintjs/fingerprintjs";
import "vite/modulepreload-polyfill";
import { mapValues, pick } from "lodash-es";

export function getCookie(name: string) {
  const value = "; " + document.cookie;
  const parts = value.split("; " + name + "=");

  if (parts.length == 2) {
    return parts.pop()!.split(";").shift();
  }
}

const fpPromise = Fingerprint2.load();

fpPromise
  .then((fp) => fp.get())
  .then((result) => {
    return fetch("/links/update/", {
      method: "POST",
      body: JSON.stringify({
        fingerprint_fields: result.components,
        fingerprint: result.visitorId,
        height: window.screen.height,
        width: window.screen.width,
      }),
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken") || "",
      },
    });
  })
  .then(() => {
    window.location.replace((window as any).destination);
  });
