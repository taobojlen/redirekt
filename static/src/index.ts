import Fingerprint2 from "fingerprintjs2";
import { pick, reduce } from "lodash";

const options: Fingerprint2.Options = {
  excludes: {
    plugins: true,
    canvas: true,
    webgl: true,
    adBlock: true,
    enumerateDevices: true,
    fonts: true,
    language: true,
    doNotTrack: true,
  },
};

export function getCookie(name: string) {
  const value = "; " + document.cookie;
  const parts = value.split("; " + name + "=");

  if (parts.length == 2) {
    return parts.pop()!.split(";").shift();
  }
}

const postDetails = async (components: Fingerprint2.Component[]) => {
  const componentsObject = reduce(
    components,
    (memo, curr) => {
      return { ...memo, [curr.key]: curr.value };
    },
    {}
  );
  const keys = [
    "webdriver",
    "colorDepth",
    "pixelRatio",
    "hardwareConcurrency",
    "timezone",
    "sessionStorage",
    "localStorage",
    "indexedDb",
    "addBehavior",
    "openDatabase",
    "platform",
    "webglVendorAndRenderer",
    "screenResolution",
    "availableScreenResolution",
  ];
  const pureContent = pick(componentsObject, keys);
  const content = {
    ...pureContent,
    touchSupport: (componentsObject as any).touchSupport.some((c: any) => !!c),
  };

  const csrfToken = getCookie("csrftoken") || "";

  await fetch("/links/update/", {
    method: "POST",
    body: JSON.stringify(content),
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
  });

  window.location.replace((window as any).destination);
};

const getDetails = () => {
  Fingerprint2.get(options, postDetails);
};

if ((window as any).requestIdleCallback) {
  (window as any).requestIdleCallback!(getDetails);
} else {
  setTimeout(getDetails, 500);
}
