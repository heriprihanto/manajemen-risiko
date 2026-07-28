import{s as at,a as _}from"./index-Cb5-83-5.js";import{B as q,R as W,a2 as F,g as M,a3 as E,p as lt,u as it,o as b,c as m,a,i as j,q as rt,m as w,j as U,t as u,a4 as V,a5 as P,r as st,P as O,Q as C,k as z,a6 as dt,w as y,_ as ut,Z as ct,y as pt,N as gt,a0 as bt,z as ft,A as p,h,H as N,J as T,W as B,M as I,E as ht}from"./index-BED9dlrk.js";import{s as H}from"./index-D3p1IG-s.js";import"./index-CcQ4q_rH.js";import"./index-RUZLvLaI.js";var vt=`
    .p-togglebutton {
        display: inline-flex;
        cursor: pointer;
        user-select: none;
        overflow: hidden;
        position: relative;
        color: dt('togglebutton.color');
        background: dt('togglebutton.background');
        border: 1px solid dt('togglebutton.border.color');
        padding: dt('togglebutton.padding');
        font-size: 1rem;
        font-family: inherit;
        font-feature-settings: inherit;
        transition:
            background dt('togglebutton.transition.duration'),
            color dt('togglebutton.transition.duration'),
            border-color dt('togglebutton.transition.duration'),
            outline-color dt('togglebutton.transition.duration'),
            box-shadow dt('togglebutton.transition.duration');
        border-radius: dt('togglebutton.border.radius');
        outline-color: transparent;
        font-weight: dt('togglebutton.font.weight');
    }

    .p-togglebutton-content {
        display: inline-flex;
        flex: 1 1 auto;
        align-items: center;
        justify-content: center;
        gap: dt('togglebutton.gap');
        padding: dt('togglebutton.content.padding');
        background: transparent;
        border-radius: dt('togglebutton.content.border.radius');
        transition:
            background dt('togglebutton.transition.duration'),
            color dt('togglebutton.transition.duration'),
            border-color dt('togglebutton.transition.duration'),
            outline-color dt('togglebutton.transition.duration'),
            box-shadow dt('togglebutton.transition.duration');
    }

    .p-togglebutton:not(:disabled):not(.p-togglebutton-checked):hover {
        background: dt('togglebutton.hover.background');
        color: dt('togglebutton.hover.color');
    }

    .p-togglebutton.p-togglebutton-checked {
        background: dt('togglebutton.checked.background');
        border-color: dt('togglebutton.checked.border.color');
        color: dt('togglebutton.checked.color');
    }

    .p-togglebutton-checked .p-togglebutton-content {
        background: dt('togglebutton.content.checked.background');
        box-shadow: dt('togglebutton.content.checked.shadow');
    }

    .p-togglebutton:focus-visible {
        box-shadow: dt('togglebutton.focus.ring.shadow');
        outline: dt('togglebutton.focus.ring.width') dt('togglebutton.focus.ring.style') dt('togglebutton.focus.ring.color');
        outline-offset: dt('togglebutton.focus.ring.offset');
    }

    .p-togglebutton.p-invalid {
        border-color: dt('togglebutton.invalid.border.color');
    }

    .p-togglebutton:disabled {
        opacity: 1;
        cursor: default;
        background: dt('togglebutton.disabled.background');
        border-color: dt('togglebutton.disabled.border.color');
        color: dt('togglebutton.disabled.color');
    }

    .p-togglebutton-label,
    .p-togglebutton-icon {
        position: relative;
        transition: none;
    }

    .p-togglebutton-icon {
        color: dt('togglebutton.icon.color');
    }

    .p-togglebutton:not(:disabled):not(.p-togglebutton-checked):hover .p-togglebutton-icon {
        color: dt('togglebutton.icon.hover.color');
    }

    .p-togglebutton.p-togglebutton-checked .p-togglebutton-icon {
        color: dt('togglebutton.icon.checked.color');
    }

    .p-togglebutton:disabled .p-togglebutton-icon {
        color: dt('togglebutton.icon.disabled.color');
    }

    .p-togglebutton-sm {
        padding: dt('togglebutton.sm.padding');
        font-size: dt('togglebutton.sm.font.size');
    }

    .p-togglebutton-sm .p-togglebutton-content {
        padding: dt('togglebutton.content.sm.padding');
    }

    .p-togglebutton-lg {
        padding: dt('togglebutton.lg.padding');
        font-size: dt('togglebutton.lg.font.size');
    }

    .p-togglebutton-lg .p-togglebutton-content {
        padding: dt('togglebutton.content.lg.padding');
    }

    .p-togglebutton-fluid {
        width: 100%;
    }
`,yt={root:function(e){var n=e.instance,i=e.props;return["p-togglebutton p-component",{"p-togglebutton-checked":n.active,"p-invalid":n.$invalid,"p-togglebutton-fluid":i.fluid,"p-togglebutton-sm p-inputfield-sm":i.size==="small","p-togglebutton-lg p-inputfield-lg":i.size==="large"}]},content:"p-togglebutton-content",icon:"p-togglebutton-icon",label:"p-togglebutton-label"},mt=q.extend({name:"togglebutton",style:vt,classes:yt}),_t={name:"BaseToggleButton",extends:F,props:{onIcon:String,offIcon:String,onLabel:{type:String,default:"Yes"},offLabel:{type:String,default:"No"},readonly:{type:Boolean,default:!1},tabindex:{type:Number,default:null},ariaLabelledby:{type:String,default:null},ariaLabel:{type:String,default:null},size:{type:String,default:null},fluid:{type:Boolean,default:null}},style:mt,provide:function(){return{$pcToggleButton:this,$parentInstance:this}}};function L(t){"@babel/helpers - typeof";return L=typeof Symbol=="function"&&typeof Symbol.iterator=="symbol"?function(e){return typeof e}:function(e){return e&&typeof Symbol=="function"&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},L(t)}function St(t,e,n){return(e=kt(e))in t?Object.defineProperty(t,e,{value:n,enumerable:!0,configurable:!0,writable:!0}):t[e]=n,t}function kt(t){var e=wt(t,"string");return L(e)=="symbol"?e:e+""}function wt(t,e){if(L(t)!="object"||!t)return t;var n=t[Symbol.toPrimitive];if(n!==void 0){var i=n.call(t,e);if(L(i)!="object")return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return(e==="string"?String:Number)(t)}var J={name:"ToggleButton",extends:_t,inheritAttrs:!1,emits:["change"],methods:{getPTOptions:function(e){var n=e==="root"?this.ptmi:this.ptm;return n(e,{context:{active:this.active,disabled:this.disabled}})},onChange:function(e){!this.disabled&&!this.readonly&&(this.writeValue(!this.d_value,e),this.$emit("change",e))},onBlur:function(e){var n,i;(n=(i=this.formField).onBlur)===null||n===void 0||n.call(i,e)}},computed:{active:function(){return this.d_value===!0},hasLabel:function(){return E(this.onLabel)&&E(this.offLabel)},label:function(){return this.hasLabel?this.d_value?this.onLabel:this.offLabel:" "},dataP:function(){return M(St({checked:this.active,invalid:this.$invalid},this.size,this.size))}},directives:{ripple:W}},xt=["tabindex","disabled","aria-pressed","aria-label","aria-labelledby","data-p-checked","data-p-disabled","data-p"],Bt=["data-p"];function Ot(t,e,n,i,f,o){var c=lt("ripple");return it((b(),m("button",w({type:"button",class:t.cx("root"),tabindex:t.tabindex,disabled:t.disabled,"aria-pressed":t.d_value,onClick:e[0]||(e[0]=function(){return o.onChange&&o.onChange.apply(o,arguments)}),onBlur:e[1]||(e[1]=function(){return o.onBlur&&o.onBlur.apply(o,arguments)})},o.getPTOptions("root"),{"aria-label":t.ariaLabel,"aria-labelledby":t.ariaLabelledby,"data-p-checked":o.active,"data-p-disabled":t.disabled,"data-p":o.dataP}),[a("span",w({class:t.cx("content")},o.getPTOptions("content"),{"data-p":o.dataP}),[j(t.$slots,"default",{},function(){return[j(t.$slots,"icon",{value:t.d_value,class:rt(t.cx("icon"))},function(){return[t.onIcon||t.offIcon?(b(),m("span",w({key:0,class:[t.cx("icon"),t.d_value?t.onIcon:t.offIcon]},o.getPTOptions("icon")),null,16)):U("",!0)]}),a("span",w({class:t.cx("label")},o.getPTOptions("label")),u(o.label),17)]})],16,Bt)],16,xt)),[[c]])}J.render=Ot;var Lt=`
    .p-selectbutton {
        display: inline-flex;
        user-select: none;
        vertical-align: bottom;
        outline-color: transparent;
        border-radius: dt('selectbutton.border.radius');
    }

    .p-selectbutton .p-togglebutton {
        border-radius: 0;
        border-width: 1px 1px 1px 0;
    }

    .p-selectbutton .p-togglebutton:focus-visible {
        position: relative;
        z-index: 1;
    }

    .p-selectbutton .p-togglebutton:first-child {
        border-inline-start-width: 1px;
        border-start-start-radius: dt('selectbutton.border.radius');
        border-end-start-radius: dt('selectbutton.border.radius');
    }

    .p-selectbutton .p-togglebutton:last-child {
        border-start-end-radius: dt('selectbutton.border.radius');
        border-end-end-radius: dt('selectbutton.border.radius');
    }

    .p-selectbutton.p-invalid {
        outline: 1px solid dt('selectbutton.invalid.border.color');
        outline-offset: 0;
    }

    .p-selectbutton-fluid {
        width: 100%;
    }
    
    .p-selectbutton-fluid .p-togglebutton {
        flex: 1 1 0;
    }
`,Pt={root:function(e){var n=e.props,i=e.instance;return["p-selectbutton p-component",{"p-invalid":i.$invalid,"p-selectbutton-fluid":n.fluid}]}},Tt=q.extend({name:"selectbutton",style:Lt,classes:Pt}),$t={name:"BaseSelectButton",extends:F,props:{options:Array,optionLabel:null,optionValue:null,optionDisabled:null,multiple:Boolean,allowEmpty:{type:Boolean,default:!0},dataKey:null,ariaLabelledby:{type:String,default:null},size:{type:String,default:null},fluid:{type:Boolean,default:null}},style:Tt,provide:function(){return{$pcSelectButton:this,$parentInstance:this}}};function At(t,e){var n=typeof Symbol<"u"&&t[Symbol.iterator]||t["@@iterator"];if(!n){if(Array.isArray(t)||(n=Q(t))||e){n&&(t=n);var i=0,f=function(){};return{s:f,n:function(){return i>=t.length?{done:!0}:{done:!1,value:t[i++]}},e:function(v){throw v},f}}throw new TypeError(`Invalid attempt to iterate non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}var o,c=!0,l=!1;return{s:function(){n=n.call(t)},n:function(){var v=n.next();return c=v.done,v},e:function(v){l=!0,o=v},f:function(){try{c||n.return==null||n.return()}finally{if(l)throw o}}}}function Vt(t){return Ct(t)||jt(t)||Q(t)||It()}function It(){throw new TypeError(`Invalid attempt to spread non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}function Q(t,e){if(t){if(typeof t=="string")return R(t,e);var n={}.toString.call(t).slice(8,-1);return n==="Object"&&t.constructor&&(n=t.constructor.name),n==="Map"||n==="Set"?Array.from(t):n==="Arguments"||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?R(t,e):void 0}}function jt(t){if(typeof Symbol<"u"&&t[Symbol.iterator]!=null||t["@@iterator"]!=null)return Array.from(t)}function Ct(t){if(Array.isArray(t))return R(t)}function R(t,e){(e==null||e>t.length)&&(e=t.length);for(var n=0,i=Array(e);n<e;n++)i[n]=t[n];return i}var Y={name:"SelectButton",extends:$t,inheritAttrs:!1,emits:["change"],methods:{getOptionLabel:function(e){return this.optionLabel?P(e,this.optionLabel):e},getOptionValue:function(e){return this.optionValue?P(e,this.optionValue):e},getOptionRenderKey:function(e){return this.dataKey?P(e,this.dataKey):this.getOptionLabel(e)},isOptionDisabled:function(e){return this.optionDisabled?P(e,this.optionDisabled):!1},isOptionReadonly:function(e){if(this.allowEmpty)return!1;var n=this.isSelected(e);return this.multiple?n&&this.d_value.length===1:n},onOptionSelect:function(e,n,i){var f=this;if(!(this.disabled||this.isOptionDisabled(n)||this.isOptionReadonly(n))){var o=this.isSelected(n),c=this.getOptionValue(n),l;if(this.multiple)if(o){if(l=this.d_value.filter(function(g){return!V(g,c,f.equalityKey)}),!this.allowEmpty&&l.length===0)return}else l=this.d_value?[].concat(Vt(this.d_value),[c]):[c];else{if(o&&!this.allowEmpty)return;l=o?null:c}this.writeValue(l,e),this.$emit("change",{originalEvent:e,value:l})}},isSelected:function(e){var n=!1,i=this.getOptionValue(e);if(this.multiple){if(this.d_value){var f=At(this.d_value),o;try{for(f.s();!(o=f.n()).done;){var c=o.value;if(V(c,i,this.equalityKey)){n=!0;break}}}catch(l){f.e(l)}finally{f.f()}}}else n=V(this.d_value,i,this.equalityKey);return n}},computed:{equalityKey:function(){return this.optionValue?null:this.dataKey},dataP:function(){return M({invalid:this.$invalid})}},directives:{ripple:W},components:{ToggleButton:J}},zt=["aria-labelledby","data-p"];function Rt(t,e,n,i,f,o){var c=st("ToggleButton");return b(),m("div",w({class:t.cx("root"),role:"group","aria-labelledby":t.ariaLabelledby},t.ptmi("root"),{"data-p":o.dataP}),[(b(!0),m(O,null,C(t.options,function(l,g){return b(),z(c,{key:o.getOptionRenderKey(l),modelValue:o.isSelected(l),onLabel:o.getOptionLabel(l),offLabel:o.getOptionLabel(l),disabled:t.disabled||o.isOptionDisabled(l),unstyled:t.unstyled,size:t.size,readonly:o.isOptionReadonly(l),onChange:function($){return o.onOptionSelect($,l,g)},pt:t.ptm("pcToggleButton")},dt({_:2},[t.$slots.option?{name:"default",fn:y(function(){return[j(t.$slots,"option",{option:l,index:g},function(){return[a("span",w({ref_for:!0},t.ptm("pcToggleButton").label),u(o.getOptionLabel(l)),17)]})]}),key:"0"}:void 0]),1032,["modelValue","onLabel","offLabel","disabled","unstyled","size","readonly","onChange","pt"])}),128))],16,zt)}Y.render=Rt;const Kt={class:"toolbar no-print"},Dt={class:"muted"},Et={key:0,class:"muted"},Nt={class:"stat-grid",style:{"margin-bottom":"16px"}},Ht={class:"stat"},qt={class:"v"},Wt={class:"stat"},Ft={class:"v"},Mt={class:"stat"},Ut={class:"v"},Jt={class:"page-card",style:{padding:"0"}},Qt={class:"muted"},Yt={class:"muted"},Zt={class:"detail"},Gt={class:"detail-head"},Xt={class:"detail-table"},te={class:"c muted",style:{width:"32px"}},ee={class:"c",style:{width:"150px"}},ne={key:1,class:"muted"},oe={__name:"SurveiHasil",setup(t){const e=ct(),n=pt(),i=gt(),f=bt(),o=B(()=>n.isAdmin),c=T(!0),l=T(null),g=T([]),v=T("all"),$=[{label:"Semua",value:"all"},{label:"Survei Publik",value:"survei"},{label:"Input Admin",value:"admin"}],Z={1:"Tidak Setuju",2:"Kurang Setuju",3:"Setuju",4:"Sangat Setuju"},A=B(()=>{var d;const s=((d=l.value)==null?void 0:d.responden)||[];return v.value==="all"?s:s.filter(S=>S.sumber===v.value)}),G=B(()=>A.value.length),X=B(()=>{const s=A.value.map(d=>d.rata_rata).filter(d=>d!=null);return s.length?(s.reduce((d,S)=>d+S,0)/s.length).toFixed(2):"–"}),K=B(()=>{var s;return((s=l.value)==null?void 0:s.total_pertanyaan)||0});function tt(s){if(!s)return"–";try{return new Date(s).toLocaleString("id-ID",{dateStyle:"medium",timeStyle:"short"})}catch{return s}}function et(s){return s==null?"secondary":s>=3?"success":"danger"}function nt(s){f.require({message:`Hapus hasil survei responden "${s.kode_responden}${s.nama_responden?" — "+s.nama_responden:""}"? Tindakan ini tidak dapat dibatalkan.`,header:"Konfirmasi Hapus",icon:"pi pi-exclamation-triangle",acceptClass:"p-button-danger",accept:async()=>{await N.delete(`/cee/survei-hasil/${s.id}`),await D(),i.add({severity:"success",summary:"Hasil survei dihapus",life:1800})}})}async function D(){c.value=!0,g.value=[];const{data:s}=await N.get("/cee/survei-hasil",{params:{opd_id:e.opdId,tahun:e.tahun}});l.value=s,c.value=!1}return ft(D),(s,d)=>{var S;return b(),m(O,null,[a("div",Kt,[a("span",Dt,u((S=p(e).opd)==null?void 0:S.nama_pd)+" — "+u(p(e).tahun),1),d[2]||(d[2]=a("div",{class:"spacer"},null,-1)),h(p(Y),{modelValue:v.value,"onUpdate:modelValue":d[0]||(d[0]=r=>v.value=r),options:$,optionLabel:"label",optionValue:"value"},null,8,["modelValue"])]),c.value?(b(),m("div",Et,"Memuat rincian hasil survei…")):(b(),m(O,{key:1},[a("div",Nt,[a("div",Ht,[a("div",qt,u(G.value),1),d[3]||(d[3]=a("div",{class:"l"},"Responden",-1))]),a("div",Wt,[a("div",Ft,u(K.value),1),d[4]||(d[4]=a("div",{class:"l"},"Pertanyaan per Responden",-1))]),a("div",Mt,[a("div",Ut,u(X.value),1),d[5]||(d[5]=a("div",{class:"l"},"Rata-rata Skor (1–4)",-1))])]),a("div",Jt,[h(p(at),{expandedRows:g.value,"onUpdate:expandedRows":d[1]||(d[1]=r=>g.value=r),value:A.value,dataKey:"id",size:"small",stripedRows:"",scrollable:""},{expansion:y(({data:r})=>[a("div",Zt,[(b(!0),m(O,null,C(l.value.kategori,x=>(b(),m("div",{key:x.id,class:"detail-kat"},[a("div",Gt,u(x.kode)+". "+u(x.nama),1),a("table",Xt,[a("tbody",null,[(b(!0),m(O,null,C(x.pertanyaan,(k,ot)=>(b(),m("tr",{key:k.id},[a("td",te,u(ot+1),1),a("td",null,u(k.pertanyaan),1),a("td",ee,[r.jawaban[k.id]!=null?(b(),z(p(H),{key:0,value:`${r.jawaban[k.id]} — ${Z[r.jawaban[k.id]]}`,severity:et(r.jawaban[k.id])},null,8,["value","severity"])):(b(),m("span",ne,"Belum dijawab"))])]))),128))])])]))),128))])]),empty:y(()=>[...d[6]||(d[6]=[a("div",{class:"muted",style:{padding:"14px"}},"Belum ada responden survei.",-1)])]),default:y(()=>[h(p(_),{expander:"",style:{width:"42px"}}),h(p(_),{field:"kode_responden",header:"Kode",style:{width:"70px"}}),h(p(_),{header:"Nama Responden",style:{minWidth:"180px"}},{body:y(({data:r})=>[I(u(r.nama_responden||"–"),1)]),_:1}),h(p(_),{header:"Jabatan",style:{minWidth:"150px"}},{body:y(({data:r})=>[I(u(r.jabatan||"–"),1)]),_:1}),h(p(_),{header:"Email",style:{minWidth:"190px"}},{body:y(({data:r})=>[a("span",Qt,u(r.email||"–"),1)]),_:1}),h(p(_),{header:"Sumber",style:{width:"120px"}},{body:y(({data:r})=>[h(p(H),{value:r.sumber==="survei"?"Survei Publik":"Input Admin",severity:r.sumber==="survei"?"info":"secondary"},null,8,["value","severity"])]),_:1}),h(p(_),{header:"Terisi",style:{width:"90px"}},{body:y(({data:r})=>[I(u(r.jumlah_jawaban)+" / "+u(K.value),1)]),_:1}),h(p(_),{header:"Rata-rata",style:{width:"90px"}},{body:y(({data:r})=>[a("strong",null,u(r.rata_rata??"–"),1)]),_:1}),h(p(_),{header:"Waktu Pengisian",style:{minWidth:"160px"}},{body:y(({data:r})=>[a("span",Yt,u(tt(r.submitted_at)),1)]),_:1}),o.value?(b(),z(p(_),{key:0,header:"",style:{width:"56px"},class:"no-print"},{body:y(({data:r})=>[h(p(ht),{icon:"pi pi-trash",text:"",rounded:"",size:"small",severity:"danger",onClick:x=>nt(r)},null,8,["onClick"])]),_:1})):U("",!0)]),_:1},8,["expandedRows","value"])])],64))],64)}}},de=ut(oe,[["__scopeId","data-v-5cd4fc8d"]]);export{de as default};
